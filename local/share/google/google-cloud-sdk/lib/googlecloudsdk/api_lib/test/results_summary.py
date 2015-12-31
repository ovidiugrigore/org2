# Copyright 2015 Google Inc. All Rights Reserved.

"""A library to build a test results summary."""

import collections

from googlecloudsdk.api_lib.test import util
from googlecloudsdk.calliope import exceptions
from googlecloudsdk.core import log
from googlecloudsdk.third_party.apitools.base import py as apitools_base


class TestOutcome(collections.namedtuple(
    'TestOutcome', ['outcome', 'axis_value', 'test_details'])):
  """A tuple to hold the outcome for a single test axis value.

  Fields:
    outcome: string containing the test outcome (e.g. 'Passed')
    axis_value: string representing one axis value within the matrix.
    test_details: string with extra details (e.g. "Incompatible architecture")
  """


# Human-freindly test outcome names
_SUCCESS = 'Passed'
_FAILURE = 'Failed'
_SKIPPED = 'Skipped'
_INCONCLUSIVE = 'Inconclusive'

# Relative sort weightings for test outcomes
_OUTCOME_SORTING = {
    _FAILURE: 10,
    _SUCCESS: 20,
    _INCONCLUSIVE: 30,
    _SKIPPED: 40,
}


def _TestOutcomeSortKey(x):
  """Transform a TestOutcome to a tuple yielding the desired sort order."""
  return tuple([_OUTCOME_SORTING[x.outcome], x.test_details, x.axis_value])


TEST_OUTCOME_FORMAT = """\
table[box](outcome.color(red=Fail, green=Pass, yellow=Inconclusive), \
axis_value:label=TEST_AXIS_VALUE, \
test_details:label=TEST_DETAILS)"""


class ToolResultsSummaryFetcher(object):
  """Creates Test Results summary using data from the Tool Results API.
  """

  def __init__(self, project, client, messages, tool_results_ids):
    """Constructs a ToolResultsSummaryFetcher.

    Args:
      project: string containing the GCE project id.
      client: ToolResults API client lib generated by apitools.
      messages: ToolResults API message classes generated by apitools.
      tool_results_ids: a ToolResultsIds object holding history & execution IDs.
    """
    self._project = project
    self._client = client
    self._messages = messages
    self._history_id = tool_results_ids.history_id
    self._execution_id = tool_results_ids.execution_id
    self._outcome_names = {
        messages.Outcome.SummaryValueValuesEnum.success: _SUCCESS,
        messages.Outcome.SummaryValueValuesEnum.failure: _FAILURE,
        messages.Outcome.SummaryValueValuesEnum.skipped: _SKIPPED,
        messages.Outcome.SummaryValueValuesEnum.inconclusive: _INCONCLUSIVE,
    }

  def FetchMatrixRollupOutcome(self):
    """Gets a test execution's rolled-up outcome from the Tool Results service.

    Returns:
      The rolled-up test execution outcome (type: toolresults_v1beta3.Outcome).

    Raises:
      HttpException if the Tool Results service reports a back-end error.
    """
    request = self._messages.ToolresultsProjectsHistoriesExecutionsGetRequest(
        projectId=self._project,
        historyId=self._history_id,
        executionId=self._execution_id)
    try:
      response = self._client.projects_histories_executions.Get(request)
      log.debug('\nTRHistoriesExecutions.Get response:\n{0}\n'.format(response))
      return response.outcome
    except apitools_base.HttpError as error:
      msg = 'Http error fetching test roll-up outcome: ' + util.GetError(error)
      raise exceptions.HttpException(msg)

  def CreateMatrixOutcomeSummary(self):
    """Fetches test results and creates a test outcome summary.

    Lists all the steps in an execution and creates a high-level outcome summary
    for each step (pass/fail/inconclusive). Each step represents a combination
    of a test execution (e.g. running the tests on a Nexus 5 in portrait mode
    using the en locale and API level 18).

    Returns:
      A list of TestOutcome objects.

    Raises:
      ToolException if the Tool Results service reports a back-end error.
    """
    outcomes = []
    steps = self._ListAllSteps()
    if not steps:
      log.warning(
          'No results found, something went wrong. Try re-running the tests.')
      return outcomes

    for step in steps:
      axes = {}
      for dimension in step.dimensionValue:
        axes[dimension.key] = dimension.value
      axis_value = ('{m}-{v}-{l}-{o}'
                    .format(m=axes.get('Model', '?'),
                            v=axes.get('Version', '?'),
                            l=axes.get('Locale', '?'),
                            o=axes.get('Orientation', '?')))
      # It's a bug in Tool Results if we get no outcome, but this guard
      # prevents a stack trace if it should happen.
      if not step.outcome:
        log.warning('Step for [{0}] had no outcome value.'.format(axis_value))
      else:
        details = self._GetStepOutcomeDetails(step)
        if details is not None:
          outcome_str = self._GetOutcomeSummaryDisplayName(step.outcome.summary)
          outcomes.append(
              TestOutcome(outcome=outcome_str,
                          axis_value=axis_value,
                          test_details=details))

    return sorted(outcomes, key=_TestOutcomeSortKey)

  def _ListAllSteps(self):
    """Lists all steps for a test execution using the Tool Results service.

    Returns:
      The full list of steps for a test execution.
    """
    response = self._ListSteps(None)
    steps = []
    steps.extend(response.steps)

    while response.nextPageToken:
      response = self._ListSteps(response.nextPageToken)
      steps.extend(response.steps)

    return steps

  def _ListSteps(self, page_token):
    """Lists one page of steps using the Tool Results service.

    Args:
      page_token: A page token to attach to the List request.

    Returns:
      A ListStepsResponse containing a single page's steps.

    Raises:
      HttpException if the Tool Results service reports a back-end error.
    """
    request = (
        self._messages.ToolresultsProjectsHistoriesExecutionsStepsListRequest(
            projectId=self._project, historyId=self._history_id,
            executionId=self._execution_id, pageSize=100, pageToken=page_token))
    try:
      response = self._client.projects_histories_executions_steps.List(request)
      log.debug('\nToolResultsSteps.List response:\n{0}\n'.format(response))
      return response
    except apitools_base.HttpError as error:
      msg = 'Http error while listing test results: ' +  util.GetError(error)
      raise exceptions.HttpException(msg)

  def _GetOutcomeSummaryDisplayName(self, outcome):
    """Transforms the outcome enum to a human readable outcome.

    Args:
      outcome: An Outcome.SummaryValueValuesEnum value.

    Returns:
      A string containing a human readable outcome.
    """
    try:
      return self._outcome_names[outcome]
    except ValueError:
      return 'Unknown'

  def _GetStepOutcomeDetails(self, step):
    """Turn test outcome counts and details into something human readable."""
    outcome = step.outcome
    summary = outcome.summary

    if summary == self._messages.Outcome.SummaryValueValuesEnum.success:
      total = 0
      for overview in step.testExecutionStep.testSuiteOverviews:
        total += overview.totalCount or 0
      if total:
        return '{t} test cases passed'.format(t=total)
      else:
        return '--'

    elif summary == self._messages.Outcome.SummaryValueValuesEnum.failure:
      if outcome.failureDetail:
        if outcome.failureDetail.crashed:
          return 'Application crashed'
        if outcome.failureDetail.timedOut:
          return 'Test timed out'
        if outcome.failureDetail.notInstalled:
          return 'App failed to install'
      return _GetFailedCountDetails(step)

    elif summary == self._messages.Outcome.SummaryValueValuesEnum.inconclusive:
      if outcome.inconclusiveDetail:
        if outcome.inconclusiveDetail.infrastructureFailure:
          return 'Infrastructure failure'
        if outcome.inconclusiveDetail.abortedByUser:
          return 'Test run aborted by user'
        if outcome.inconclusiveDetail.nativeCrash:
          return 'A native process crashed on the device'
      return 'Unknown reason'

    elif summary == self._messages.Outcome.SummaryValueValuesEnum.skipped:
      if outcome.skippedDetail:
        if outcome.skippedDetail.incompatibleDevice:
          return 'Incompatible device/OS combination'
        if outcome.skippedDetail.incompatibleArchitecture:
          return 'App does not support the device architecture'
        if outcome.skippedDetail.incompatibleAppVersion:
          return 'App does not support the OS version'
      return 'Unknown reason'

    else:
      return 'Unknown outcome'


def _GetFailedCountDetails(step):
  """Build a string with status count sums for a step's testSuiteOverviews."""
  if not step.testExecutionStep:
    return 'Unknown failure'
  total = 0
  error = 0
  failed = 0
  skipped = 0
  for overview in step.testExecutionStep.testSuiteOverviews:
    total += overview.totalCount or 0
    error += overview.errorCount or 0
    failed += overview.failureCount or 0
    skipped += overview.skippedCount or 0

  if total:
    msg = '{f} test cases failed'.format(f=failed)
    passed = total - error - failed - skipped
    if passed:
      msg = '{m}, {p} passed'.format(m=msg, p=passed)
    if error:
      msg = '{m}, {e} errors'.format(m=msg, e=error)
    if skipped:
      msg = '{m}, {s} skipped'.format(m=msg, s=skipped)
    return msg
  else:
    return 'Test failed to run'