def create_policy_comparison_prompt(policies, insurance_type):
    """Create a structured prompt to compare insurance policies with markdown table format."""
    num_policies = len(policies)
    if insurance_type.lower() == "auto":
        prompt = (
            f"You are a financial expert specializing in {insurance_type} insurance. "
            f"Please compare the following {num_policies} {insurance_type} insurance policies in detail. "
            "Your response should include:\n"
            "1. A **Comparison Report** in the form of a markdown table. The table should have the following columns: "
            "`Provider Name`, `Coverage Summary`, `Coverage Limit`, `Monthly Premium`, `Collision Deductible`, and `Comprehensive Deductible`.\n"
            "   - **Coverage Summary**: Provide a brief overview (2-3 sentences) highlighting only the key coverage aspects of each policy, such as types of services covered, preventive care, mental health services, and any additional benefits. **Do not include the coverage limit or deductible information in this section.**\n"
            "2. A **Summary of Key Differences**: After the table, provide a brief summary highlighting the key differences between the policies, "
            f"focusing on {insurance_type}-specific factors such as significant variations in coverage, affordability, premiums, deductibles, coverage limits, and additional benefits. "
            "Explain how these differences impact the overall value and suitability of each policy for different types of individuals or families.\n"
            f"3. **{insurance_type.capitalize()} Insurance Recommendations**: Indicate which {insurance_type} policy is better and why, considering factors like affordability, coverage, benefits, and specific user needs.\n"
            "4. **Explanations**: For each policy, provide an introductory paragraph summarizing the overall strengths and weaknesses of the policy, "
            "and then format the pros and cons in bullet points as follows:\n"
            "- **Pros**:\n"
            "  - List the benefits of the policy, such as lower premiums, higher coverage, or better terms.\n"
            "- **Cons**:\n"
            "  - List the downsides of the policy, such as higher premiums, lower coverage, or less favorable terms.\n\n"
            "Please format the comparison as a table using the following format:\n"
            "| Provider Name | Coverage Summary | Coverage Limit | Monthly Premium | Collision Deductible | Comprehensive Deductible |\n"
            "| ------------- | ---------------- | -------------- | --------------- | -------------------- | ------------------------ |\n"
        )
        for idx, policy in enumerate(policies):
            provider = policy.get("provider", "N/A")
            coverage = policy.get("coverage", "N/A")
            coverage_limit = policy.get("coverage_limit", "N/A")
            premium = policy.get("premium", "N/A")
            collision_deductible = policy.get("deductible", {}).get("collision", "N/A")
            comprehensive_deductible = policy.get("deductible", {}).get("comprehensive", "N/A")

            prompt += (
                f"| {provider} | {coverage} | {coverage_limit} | "
                f"{premium} | {collision_deductible} | {comprehensive_deductible} |\n"
            )
        return prompt  # Ensure prompt is returned for auto insurance

    else:
        prompt = (
            f"You are a financial expert specializing in {insurance_type} insurance. "
            f"Please compare the following {num_policies} {insurance_type} insurance policies in detail. "
            "Your response should include:\n"
            "1. A **Comparison Report** in the form of a markdown table. The table should have the following columns: "
            "`Provider Name`, `Coverage Summary`, `Coverage Limit`, `Monthly Premium`, and `Deductibles`.\n"
            "   - **Coverage Summary**: Provide a brief overview (2-3 sentences) highlighting only the key coverage aspects of each policy, such as types of services covered, preventive care, mental health services, and any additional benefits. **Do not include the coverage limit or deductible information in this section.**\n"
            "2. A **Summary of Key Differences**: After the table, provide a brief summary highlighting the key differences between the policies, "
            f"focusing on {insurance_type}-specific factors such as significant variations in coverage, affordability, premiums, deductibles, coverage limits, and additional benefits. "
            "Explain how these differences impact the overall value and suitability of each policy for different types of individuals or families.\n"
            f"3. **{insurance_type.capitalize()} Insurance Recommendations**: Indicate which {insurance_type} policy is better and why, considering factors like affordability, coverage, benefits, and specific user needs.\n"
            "4. **Explanations**: For each policy, provide an introductory paragraph summarizing the overall strengths and weaknesses of the policy, "
            "and then format the pros and cons in bullet points as follows:\n"
            "- **Pros**:\n"
            "  - List the benefits of the policy, such as lower premiums, higher coverage, or better terms.\n"
            "- **Cons**:\n"
            "  - List the downsides of the policy, such as higher premiums, lower coverage, or less favorable terms.\n\n"
            "Please format the comparison as a table using the following format:\n"
            "| Provider Name | Coverage Summary | Coverage Limit | Monthly Premium | Deductibles |\n"
            "| ------------- | ----------------- | -------------- | --------------- | ----------- |\n"
        )
        for idx, policy in enumerate(policies):
            provider = policy.get("provider", "N/A")
            coverage = policy.get("coverage", "N/A")
            coverage_limit = policy.get("coverage_limit", "N/A")
            premium = policy.get("premium", "N/A")
            deductible = policy.get("deductible", "N/A")

            prompt += (
                f"| {provider} | {coverage} | {coverage_limit} | "
                f"{premium} | {deductible} |\n"
            )
        return prompt  # Ensure prompt is returned for other insurance types
