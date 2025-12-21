from collections import defaultdict
from typing import DefaultDict, List, Tuple
from langchain_core.documents import Document

from app.pydantic_models.data_model import PreferredIntent
from app.utils.envs import Envs


class ResultBalancer:
    """
    This is class is responsible for balancing the final selection of documents
    based on the greedy selection method and the user's preferred intent.
    It slowly penalizes documents that do not belong to preferred test types to ensure
    a diverse set of relevant balanced recommendations.
    """

    def balance_penalty(
        self,
        test_type: list[str],
        appearance_counts: DefaultDict[str, int],
        preferred_intent: PreferredIntent
    ) -> float:
        penalties = []

        for t in test_type:
            if t in preferred_intent.preferred_test_types:
                penalties.append(0.02 * max(0, appearance_counts[t] - 2))
            else:
                penalties.append(0.08 * max(0, appearance_counts[t] - 1))

        return min(penalties) if penalties else 0.0

    def update_counts(self, test_type, appearance_counts):
        for t in test_type:
            appearance_counts[t] += 1

    def balance_selection(
        self,
        reranked_docs: List[Tuple[Document, float]],
        intent: PreferredIntent
    ) -> List[Document]:
        if not reranked_docs:
            return []
        
        final_docs = []
        appearance_counts = defaultdict(int)
        RATIO = 0.55
        top_score = reranked_docs[0][1]
        adjusted_candidates = []

        for doc, score in reranked_docs:
            norm_score = score / top_score
            penalty = self.balance_penalty(
                doc.metadata["test_type"],
                appearance_counts,
                intent
            )
            adjusted_score = norm_score - penalty
            adjusted_candidates.append((adjusted_score, doc))

        adjusted_candidates.sort(key=lambda x: x[0], reverse=True)

        unique_docs = set()
        for adj_score, doc in adjusted_candidates:
            decay = (adj_score < (top_score * RATIO))
            
            if (len(final_docs) >= Envs.MIN_RESULTS and decay):
                break
            
            if doc.metadata["url"] in unique_docs:
                continue
            
            final_docs.append(doc)
            self.update_counts(doc.metadata["test_type"], appearance_counts)
            unique_docs.add(doc.metadata["url"])

            if len(final_docs) >= Envs.MAX_RESULTS:
                break

        return final_docs
