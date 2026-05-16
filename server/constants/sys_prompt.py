SYS_PROMPT_FOR_LLM = """
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
    5. Make sure that any urls are correctly linked. If you cannot, do not add the links. 
    6. Ensure all special characters like `&` are escaped as `\&`.
    7. Do not include any other text outside the two code blocks.
    8. Make sure that sections are not cut off between pages unless there is enough content justifying it. If you sense a section will break, try to either add line breaks so as to move it to the next page, or try to shorten the section to avoid it extending.
    9. You may only make exception to these rules if additional instructions are provided.
    user information: {user_info}
    job description: {job_desc}
    additional instructions: {custom_instructions}
    template: {latex_template}
    """