import json
import re

# --- Simulated AI Models and Tools ---

def mock_llm(prompt: str) -> str:
    """
    A mock Large Language Model (LLM) that simulates basic understanding and generation.
    In a real scenario, this would be an API call to OpenAI, Llama, etc.
    """
    print(f"[LLM Call] Input: '{prompt[:70]}...'\n") # Log LLM interaction
    
    if "identify entities and required data types" in prompt:
        # Simulates LLM's ability to extract intent and entities for planning
        if "Company A" in prompt:
            return json.dumps({"entity": "Company A", "data_needed": ["stock_price", "news_headlines"]})
        elif "Company B" in prompt:
            return json.dumps({"entity": "Company B", "data_needed": ["stock_price"]})
        else:
            return json.dumps({"entity": "Unknown", "data_needed": []})
    
    elif "Synthesize an answer using" in prompt:
        # Simulates LLM's ability to synthesize information into a coherent answer
        entity_name_match = re.search(r"EntityName: '([^']+)'", prompt)
        entity_name = entity_name_match.group(1) if entity_name_match else "Unknown Company"

        gathered_data_match = re.search(r"Gathered Data: ({.*})", prompt, re.DOTALL)
        gathered_data = json.loads(gathered_data_match.group(1)) if gathered_data_match else {}

        response_parts = [f"Based on your query for {entity_name}:"]
        if "stock_price" in gathered_data:
            response_parts.append(f"  - {gathered_data['stock_price']}")
        if "news_headlines" in gathered_data:
            response_parts.append(f"  - {gathered_data['news_headlines']}")
        
        if not gathered_data:
            response_parts.append("  - I couldn't find specific data for this request.")
        
        response_parts.append("\nThis information was gathered by combining general knowledge and specific data lookups.")
        
        return "\n".join(response_parts)
    
    # Fallback for general queries not requiring specific tools
    return f"I am a mock LLM. For '{prompt[:50]}...', I can provide general information but lack specific tools for this query."

def data_lookup_tool(data_type: str, entity: str) -> str:
    """
    A simulated enterprise tool for looking up specific data (e.g., from a database, API).
    This represents a 'tool' that an agent can invoke.
    """
    print(f"[Tool Call] Looking up '{data_type}' for '{entity}'...\n") # Log tool interaction
    if entity == "Company A":
        if data_type == "stock_price":
            return "Current stock price of Company A: $150.25 (up 1.5% today)"
        elif data_type == "news_headlines":
            return "Recent news for Company A: Announced new product line, positive market reaction, Q3 earnings beat expectations."
    elif entity == "Company B":
        if data_type == "stock_price":
            return "Current stock price of Company B: $99.99 (stable)"
    return f"No specific '{data_type}' data found for '{entity}'."

# --- Enterprise AI Agent Logic ---

def enterprise_ai_agent(user_query: str) -> str:
    """
    This function acts as the 'Smart Agent'. It orchestrates the use of
    the mock LLM and the data lookup tool to answer a complex query.
    This demonstrates the 'agent logic' concept from the article.
    """
    print(f"\n>>> Agent received query: '{user_query}'")
    
    # Step 1: Use LLM to understand the query, identify entities, and required data types.
    # The agent uses the LLM as a 'brain' for planning and intent recognition.
    print("\n--- Agent Step 1: Understanding Query with LLM (Planning) ---")
    llm_analysis_prompt = (
        f"Analyze this query: '{user_query}'. "
        "Identify the main entity/company mentioned and the specific types of data needed. "
        "Respond in JSON format with 'entity' and a list of 'data_needed'."
    )
    llm_response_str = mock_llm(llm_analysis_prompt)
    
    try:
        llm_analysis = json.loads(llm_response_str)
        entity = llm_analysis.get("entity", "Unknown")
        data_needed = llm_analysis.get("data_needed", [])
    except json.JSONDecodeError:
        print("[Agent Error] Failed to parse LLM analysis. Returning generic error.")
        return "Sorry, I couldn't understand your request properly."

    if entity == "Unknown" or not data_needed:
        print("[Agent Decision] Couldn't identify specific entities or data needed. Falling back to LLM for general response.")
        return mock_llm(f"Provide a general answer for: '{user_query}'")

    print(f"[Agent Decision] Identified entity: '{entity}', data needed: {data_needed}")

    # Step 2: Execute actions based on the plan (use tools).
    # The agent intelligently decides which tools to call based on the identified data_needed.
    print("\n--- Agent Step 2: Gathering Information with Tools (Execution) ---")
    gathered_info = {}
    for data_type in data_needed:
        tool_result = data_lookup_tool(data_type, entity)
        gathered_info[data_type] = tool_result
        print(f"  - Gathered '{data_type}': {tool_result}")

    # Step 3: Use LLM again to synthesize a final, coherent answer
    # using the original query and the gathered information. This is the 'reasoning' part.
    print("\n--- Agent Step 3: Synthesizing Final Answer with LLM (Reasoning) ---")
    synthesis_prompt = (
        f"Synthesize an answer for the original query: '{user_query}'. "
        f"Use the following information:\n"
        f"  - EntityName: '{entity}'\n"
        f"  - Gathered Data: {json.dumps(gathered_info)}"
    )
    final_answer = mock_llm(synthesis_prompt)
    
    print("\n<<< Agent Final Answer >>>")
    return final_answer

# --- Example Usage ---
if __name__ == "__main__":
    print("\n" + "="*80)
    print("DEMO 1: Query requiring both LLM planning and tool usage")
    print("="*80)
    query1 = "What is the current stock price of Company A and what are its recent news headlines?"
    print(enterprise_ai_agent(query1))

    print("\n" + "="*80)
    print("DEMO 2: Query requiring only specific data lookup")
    print("="*80)
    query2 = "Tell me about the stock price of Company B."
    print(enterprise_ai_agent(query2))

    print("\n" + "="*80)
    print("DEMO 3: Query not covered by specific tools, falls back to general LLM")
    print("="*80)
    query3 = "What is the weather like today in Istanbul?"
    print(enterprise_ai_agent(query3))
