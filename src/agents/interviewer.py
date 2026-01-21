"""
Interviewer Module

This module conducts structured interviews with simulated agents
based on their experiences.
"""

from typing import List, Dict, Any, Optional
import os

from ..llm.gemini_client import GeminiClient
from ..utils.logger import get_logger

logger = get_logger(__name__)


class Interviewer:
    """
    Conducts structured interviews with user agents.
    
    This class poses questions to agents based on their simulated experiences
    and collects their responses for analysis.
    
    Attributes:
        llm_client (GeminiClient): The LLM client for interview simulation
        prompt_template (str): Template for interview prompts
        questions (List[str]): List of interview questions
    """
    
    def __init__(
        self,
        llm_client: GeminiClient,
        questions: Optional[List[str]] = None
    ):
        """
        Initialize the interviewer.
        
        Args:
            llm_client: An initialized Gemini client instance
            questions: Optional list of interview questions
        """
        self.llm_client = llm_client
        self.prompt_template = self._load_prompt_template()
        self.questions = questions or []
        logger.info("Interviewer initialized")
    
    def _load_prompt_template(self) -> str:
        """
        Load the interview prompt template from file.
        
        Returns:
            The prompt template as a string
        """
        template_path = os.path.join(
            os.path.dirname(__file__),
            "..", "llm", "prompts", "interview.txt"
        )
        
        with open(template_path, "r") as f:
            return f.read()
    
    def set_questions(self, questions: List[str]) -> None:
        """
        Set or update the interview questions.
        
        Args:
            questions: List of question strings
        """
        self.questions = questions
        logger.info(f"Updated interview questions: {len(questions)} questions loaded")
    
    def ask_question(
        self,
        agent: str,
        experience: str,
        question: str,
        product: str = "tent",
        agent_id: Optional[int] = None
    ) -> str:
        """
        Ask a single question to an agent about their experience.
        
        Args:
            agent: The agent description/persona
            experience: The agent's simulated experience
            question: The question to ask
            product: The product being discussed
            agent_id: Optional agent ID for analytics tracking
            
        Returns:
            The agent's answer to the question
        """
        logger.debug("Asking question to agent")
        
        prompt = self.prompt_template.format(
            agent_description=agent,
            experience=experience,
            question=question,
            product=product
        )
        
        answer = self.llm_client.run(prompt, _stage="interviews", _agent_id=str(agent_id) if agent_id is not None else None)
        logger.debug("Received answer from agent")
        
        return answer
    
    def conduct_interview(
        self,
        agent: str,
        experience: str,
        product: str = "tent",
        agent_id: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Conduct a full interview with all configured questions.
        
        Args:
            agent: The agent description/persona
            experience: The agent's simulated experience
            product: The product being discussed
            agent_id: Optional agent ID for analytics tracking
            
        Returns:
            List of Q&A dictionaries
        """
        logger.info(f"Conducting interview with {len(self.questions)} questions")
        
        qa_pairs = []
        
        for idx, question in enumerate(self.questions, 1):
            logger.debug(f"Processing question {idx}/{len(self.questions)}")
            
            answer = self.ask_question(agent, experience, question, product, agent_id=agent_id)
            
            qa_pairs.append({
                "question": question,
                "answer": answer
            })
        
        logger.info(f"Interview completed: {len(qa_pairs)} Q&A pairs generated")
        return qa_pairs
    
    def conduct_multiple_interviews(
        self,
        experiences: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Conduct interviews with multiple agents.
        
        Args:
            experiences: List of experience dictionaries containing
                        agent, experience, and product information
            
        Returns:
            List of interview results with agent context
        """
        logger.info(f"Conducting interviews for {len(experiences)} agents")
        
        results = []
        
        for idx, exp_data in enumerate(experiences, 1):
            logger.debug(f"Interviewing agent {idx}/{len(experiences)}")
            
            agent_id = exp_data.get("agent_id", idx-1)
            qa_pairs = self.conduct_interview(
                agent=exp_data["agent"],
                experience=exp_data["experience"],
                product=exp_data.get("product", "tent"),
                agent_id=agent_id
            )
            
            results.append({
                "agent_id": agent_id,
                "agent": exp_data["agent"],
                "experience": exp_data["experience"],
                "product": exp_data.get("product", "tent"),
                "interview": qa_pairs
            })
        
        logger.info(f"Completed {len(results)} interviews")
        return results
    
    def ask_followup_question(
        self,
        agent: str,
        experience: str,
        previous_qa: List[Dict[str, str]],
        followup_question: str,
        product: str = "tent"
    ) -> str:
        """
        Ask a follow-up question based on previous answers.
        
        Args:
            agent: The agent description/persona
            experience: The agent's simulated experience
            previous_qa: List of previous Q&A pairs
            followup_question: The follow-up question
            product: The product being discussed
            
        Returns:
            The agent's answer to the follow-up question
        """
        logger.debug("Asking follow-up question")
        
        # Build context from previous Q&A
        qa_context = "\n\n".join([
            f"Q: {qa['question']}\nA: {qa['answer']}"
            for qa in previous_qa
        ])
        
        enhanced_experience = f"{experience}\n\nPrevious Interview:\n{qa_context}"
        
        return self.ask_question(agent, enhanced_experience, followup_question, product)
