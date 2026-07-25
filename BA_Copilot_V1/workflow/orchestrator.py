from workflow.state import WorkflowState
from agents.analyzer import RequirementAnalyzer
from agents.user_story import UserStoryAgent
from agents.acceptance_criteria import AcceptanceCriteriaAgent
from agents.gap_analysis import GapAnalysisAgent
from agents.effort_estimation import EffortEstimationAgent
from agents.review import ReviewAgent
from agents.refinement import RefinementAgent

class WorkflowOchestrator:

    def __init__(self):
        
        self.analyzer = RequirementAnalyzer()
        self.user_story_agent = UserStoryAgent()
        self.acceptance_criteria_agent = AcceptanceCriteriaAgent()
        self.gap_analysis_agent = GapAnalysisAgent()
        self.effort_agent = EffortEstimationAgent()
        self.review_agent = ReviewAgent()
        self.refinement_agent = RefinementAgent()

    def run(self, requirement: str):

        state = WorkflowState()

        state.analysis = self.analyzer.analyze(requirement)

        state.stories = self.user_story_agent.generate(state.analysis)

        state.acceptance_criteria = self.acceptance_criteria_agent.generate(state.stories)

        state.story_gaps = self.gap_analysis_agent.generate(state.stories)

        effort_input = {
            "analysis": state.analysis,
            "stories": state.stories,
            "acceptance_criteria": state.acceptance_criteria
        }

        state.effort_estimation = self.effort_agent.generate(effort_input)

        review_input = {
            "analysis": state.analysis,
            "stories": state.stories,
            "acceptance_criteria": state.acceptance_criteria,
            "story_gaps": state.story_gaps,
            "effort_estimation": state.effort_estimation
        }

        state.review = self.review_agent.generate(review_input)

        state.refinement = self.refinement_agent.generate(state.review)

        return state