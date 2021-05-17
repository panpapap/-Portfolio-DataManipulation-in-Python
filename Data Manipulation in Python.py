#!/usr/bin/env python
# coding: utf-8

# In[52]:


import pandas as pd


# In[53]:


#change the data directory accordingly
df = pd.read_excel('D:\PORTFOLIO\Data_Manipulation/Survey_edited.xlsx', sheet_name="Edited_Data")
df


# In[54]:


#Duplicate dataset for necceasry edit later
df_mod = df.copy()
df_mod


# In[55]:


#drop unnecessary columns
columns_to_drop = ['Start Date', 'End Date', 'Email Address', 'First Name', 'Last Name', 'Custom Data 1']
columns_to_drop


# In[56]:


df_mod = df_mod.drop(columns=columns_to_drop)
df_mod


# In[57]:


id_vars = list(df_mod.columns)[ : 8]
value_vars = list(df_mod.columns)[8 : ]


# In[58]:


#Unpivot data
df_melted = df_mod.melt(id_vars=id_vars, value_vars = value_vars, var_name="Question + Subquestion", value_name="Answer")
df_melted


# In[59]:


questions_import = pd.read_excel('D:\PORTFOLIO\Data_Manipulation/Survey_edited.xlsx', sheet_name="Question")
questions_import


# In[60]:


questions = questions_import.copy()
questions.drop(columns=["Raw Question", "Raw Subquestion", "Subquestion"], inplace=True)
questions


# In[61]:


#left join dataset with questions and subquestions
df_merged = pd.merge(left=df_melted, right=questions, how="left", left_on="Question + Subquestion", right_on="Question + Subquestion")
print("Original Data", len(df_melted))
print("Merged Data", len(df_merged))
df_merged


# In[62]:


respondents = df_merged[df_merged["Answer"].notna()]
respondents = respondents.groupby("Question")["Respondent ID"].nunique().reset_index()
respondents.rename(columns={"Respondent ID":"Respondents"}, inplace=True)
respondents


# In[63]:


#left join number of responds 
df_merged_two = pd.merge(left=df_merged, right=respondents, how="left", left_on="Question", right_on="Question")
print("Original Data", len(df_merged))
print("Merged Data", len(df_merged_two))
df_merged_two


# In[64]:


same_answer = df_merged # [dataset_merged["Answer"].notna()]
same_answer = same_answer.groupby(["Question + Subquestion", "Answer"])["Respondent ID"].nunique().reset_index()
same_answer.rename(columns={"Respondent ID":"Same Answer"}, inplace=True)
same_answer


# In[65]:


#left join the number of same answer
df_merged_three = pd.merge(left=df_merged_two, right=same_answer, how="left", left_on=["Question + Subquestion", "Answer"], right_on=["Question + Subquestion", "Answer"])
df_merged_three["Same Answer"].fillna(0, inplace=True)
print("Original Data", len(df_merged_two))
print("Merged Data", len(df_merged_three))
df_merged_three


# In[66]:


#rename the columns
output = df_merged_three.copy()
output.rename(columns={"Identify which division you work in. - Response":"Division Primary", "Identify which division you work in. - Other (please specify)":"Division Secondary", "Which of the following best describes your position level? - Response":"Position", "Which generation are you apart of? - Response":"Generation", "Please select the gender in which you identify. - Response":"Gender", "Which duration range best aligns with your tenure at your company? - Response":"Tenure", "Which of the following best describes your employment type? - Response":"Employment Type"}, inplace=True)
output


# In[67]:


#change the data directory accordingly
output.to_excel("D:\PORTFOLIO\Data_Manipulation\Final_Output.xlsx", index=False)


# In[ ]:




