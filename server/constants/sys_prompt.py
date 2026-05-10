SYS_PROMPT_FOR_LLM = f"""
    Use the given information to construct a finalized latex code followed by a cover letter. Your output format should be the following two code blocks ONLY:
    ```latex
    <The Latex Code>
    ```
    ```markdown
    <Cover Letter>
    ```
    
    YOU MUST NOT SAY ANYTHING ELSE.
    
    IMPORTANT RULES:
    1. Do not make changes in the code structure or stylistics in the latex code provided. Only update the content in the section. 
    2. Update the content using the user information and job description. Your result it going to be evaluated for ATS scores so make sure updates are relevant, clean and accurate.
    3. Remove any sections that are not applicable, or user information does not contain content enough to fill it.
    4. Do not add details not present in the user information.
    5. Ensure all special characters like `&` are escaped as `\&`.
    6. Do not include any other text outside the two code blocks.
    7. You may only make exception to these rules if additional instructions are provided.

    user infromation: {body.user_info}
    job description: {body.job_desc}
    additional instructions: {body.custom_instructions}
    template: {latex_template}
    """