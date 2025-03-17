from datetime import datetime

SYSTEM_PROMPT = f"""\
You are an expert researcher. Today is {datetime.now().strftime('%B %d, %Y')}. \
Follow these instructions when responding:
- You may be asked to research subjects that is after your knowledge cutoff, \
  assume the user is right when presented with news.
- The user is a highly experienced analyst, no need to simplify it, be as \
  detailed as possible and make sure your response is correct.
- Be highly organized.
- Suggest solutions that I didn't think about.
- Be proactive and anticipate my needs.
- Treat me as an expert in all subject matter.
- Mistakes erode my trust, so be accurate and thorough.
- Provide detailed explanations, I'm comfortable with lots of detail.
- Value good arguments over authorities, the source is irrelevant.
- Consider new technologies and contrarian ideas, not just the conventional \
  wisdom.
- You may use high levels of speculation or prediction, just flag it for me.\
"""

USER_PROMPT__SERP_QUERY_GENERATION = """\
Given the following prompt from the user, generate a list of SERP queries to \
research the topic. Return a maximum of {num_queries} queries, but feel free \
to return less if the original prompt is clear. Make sure each query is \
unique and not similar to each other. Your query must be not more than 10 \
keywords long.

{query_addon}
"""

USER_PROMPT__QUERY_GENERATION_ADDON__AUTO_REFINEMENT_QUERY = """\
If the user query is unclear, please clarify the question yourself by making \
assumptions that'll provide the best outcome.

User Query:
{user_query}\
"""

USER_PROMPT__QUERY_GENERATION_ADDON__PREVIOUS_RESEARCH_DETAILS = """\
Previous Research Goal:
{previous_research_goal}

Learnings:
{learnings}

Follow-up Questions from Learnings:
{follow_up_questions}\
"""

USER_PROMPT__QUERY_REFINEMENT = """\
Given the following query from the user, ask some follow up questions to \
clarify the research direction. Return a maximum of {num_questions} \
questions, but feel free to return less if the original query is clear:

User Query:
<query>{query}</query>\
"""

USER_PROMPT__LEARNING_GENERATION = """\
Given the following contents from a SERP search for the query, generate a list \
of learnings from the contents. Return a maximum of {num_learnings} learnings, \
but feel free to return less if the contents are clear. Make sure each \
learning is unique and not similar to each other. The learnings should be \
concise and to the point, as detailed and information dense as possible. Make \
sure to include any entities like people, places, companies, products, things, \
etc. in the learnings, as well as any exact metrics, numbers, or dates. If the \
SERP data contains any citations, make sure to preserve them in your response. \
The learnings will be used to research the topic further.

SERP Query:
<query>{serp_query}</query>

SERP Data:
<data>{serp_data}</data>
"""

USER_PROMPT__REPORT_GENERATION = """\
Given the following from the user, write a final report on the topic \
using the learnings from research. Make it as as detailed as possible, aim for \
3 or more pages, include ALL the learnings from research. Make sure to \
preserve the citations from the learnings in your response. The report should \
be well-organized and structured, with a clear introduction, body, and \
conclusion.

Original User Query:
<prompt>{user_query}</prompt>

Learnings:
<learnings>{learnings}</learnings>
"""
