import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np


# page configuration
st.set_page_config(page_title="Dashboard", page_icon=":bar_chart:", layout="wide")


# ~ importing data
department = pd.read_csv("dataset/departments.csv")
employees = pd.read_csv("dataset/employees.csv")
projects = pd.read_csv("dataset/projects.csv")
inventory = pd.read_csv("dataset/inventory.csv")
marketing_campaign = pd.read_csv("dataset/marketing_campaigns.csv")
project_employees = pd.read_csv("dataset/project_employees.csv")
tasks = pd.read_csv("dataset/tasks.csv")
transactions = pd.read_csv("dataset/transactions.csv")


#! starting the dashboard

st.markdown(
    "<h1 style='text-align: center';> Company Dashboard</h1>", unsafe_allow_html=True
)

# . tabs for different sections
(
    employees_sections,
    projects_sections,
    transactions_sections,
    marketing_sections,
    tasks_sections,
) = st.tabs(["Employees", "Projects", "Transactions", "Marketing Campaigns", "Tasks"])


# ? Employees Tab
with employees_sections:
    employees_department = pd.read_csv("dataset/employees_department.csv")
    st.header("Employees analysis")
    # number of employees in each department

    fig = px.bar(
        data_frame=employees_department,
        x="name",
        color="name",
        title="Number of Employees per Department",
    )
    st.plotly_chart(fig, use_container_width=True)

    eng, marketing, sales, hr, finance = st.columns([0.2, 0.2, 0.2, 0.2, 0.2])

    dep_section_num = employees_department["name"].value_counts()

    with eng:
        st.markdown("#### Engineering Employees")
        st.metric("Number of Engineering Employees", dep_section_num["Engineering"])

    with marketing:
        st.markdown("#### Marketing Employees")
        st.metric("Number of Marketing Employees", dep_section_num["Marketing"])

    with sales:
        st.markdown("#### Sales Employees")
        st.metric("Number of Sales Employees", dep_section_num["Sales"])

    with hr:
        st.markdown("#### HR Employees")
        st.metric("Number of HR Employees", dep_section_num["Human Resources"])

    with finance:
        st.markdown("#### Finance Employees")
        st.metric("Number of Finance Employees", dep_section_num["Finance"])

    # . average salary per department
    salary_average = employees_department.groupby("name")["salary"].mean()

    salary_graph, salary_mean_info = st.columns([0.7, 0.3])

    with salary_graph:
        fig_salary = px.bar(
            data_frame=salary_average.reset_index(),
            x="name",
            y="salary",
            color="name",
            title="Average Salary per Department",
        )
        st.plotly_chart(fig_salary, use_container_width=True)

    with salary_mean_info:
        st.subheader("Average Salary Information")
        avg_salaries = salary_average.values
        st.metric("Average Engineering Salary", f"${avg_salaries[0]:.2f}")
        st.metric("Average Finance Salary", f"${avg_salaries[1]:.2f}")
        st.metric("Average HR Salary", f"${avg_salaries[2]:.2f}")
        st.metric("Average Marketing Salary", f"${avg_salaries[3]:.2f}")
        st.metric("Average Sales Salary", f"${avg_salaries[4]:.2f}")

    highest_salary, num_of_new_hires = st.columns([0.5, 0.5])

with highest_salary:
    # . the hights employee take salary salary
    st.subheader("Highest Salary Employee")
    highest_salary_employee = employees_department.loc[
        employees_department["salary"].idxmax()
    ]
    st.write(f"**Name:** {highest_salary_employee['full_name']}")
    st.write(f"**Position:** {highest_salary_employee['position']}")
    st.write(f"**Department:** {highest_salary_employee['name']}")

with num_of_new_hires:
    st.subheader("New Hires in Last year")
    employees["hire_date"] = pd.to_datetime(employees["hire_date"])
    last_year = pd.Timestamp.now() - pd.DateOffset(year=2020, month=9)
    new_hires_count = employees[employees["hire_date"] > last_year].shape[0]
    st.metric("Number of New Hires", new_hires_count)


# ././///////// projects sections /////////////

with projects_sections:
    st.header("Projects Analysis")
    project_projEm = pd.read_csv("dataset/project_projEm.csv")
    project_process = project_projEm["status"].value_counts()

    fig = px.bar(data_frame=project_process, color=project_process.index)
    st.plotly_chart(fig, use_container_width=True)

    completed, in_progress, Planned = st.columns([0.3, 0.3, 0.3])

    with completed:
        st.subheader("Completed Projects")
        st.metric("Number of Completed Projects", project_process["Completed"])

    with in_progress:
        st.subheader("In Progress Projects")
        st.metric("Number of In Progress Projects", project_process["In Progress"])

    with Planned:
        st.subheader("Planned Projects")
        st.metric("Number of Planned Projects", project_process["Planned"])

    # highest_budget, empl_num_each_pro = st.columns([0.5,0.5])

    # with highest_budget:
    st.subheader("Highest Budget Project")
    highest_budget_project = projects.loc[projects["budget"].idxmax()]
    st.write(f"**Project Name:** {highest_budget_project['project_name']}")
    st.write(f"**Client ID:** {highest_budget_project['client_id']}")
    st.write(f"**Budget:** ${highest_budget_project['budget']}")

    # with empl_num_each_pro:
    st.subheader("Number of Employees in Each Project")
    emp_count = (
        project_projEm.groupby("project_name")["employee_id"].nunique().reset_index()
    )
    fig2 = px.bar(
        data_frame=emp_count,
        x="project_name",
        y="employee_id",
        color="project_name",
        title="Employees per Project",
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("percentage for Complet project")
    fig = px.pie(data_frame=project_process, names=project_process.index, hole=0.3)
    fig.update_traces(textinfo="percent+label+text")

    st.plotly_chart(fig, use_container_width=True)


with transactions_sections:
    st.header("Transaction analysis")

    transaction_project = pd.read_csv("dataset/transaction_project.csv")
    transaction_project["type"] = (
        transaction_project["type"]
        .replace("Invoice", "Income")
        .replace("Estimate", "Expense")
    )

    trans_summary = transaction_project.groupby("type")["amount"].sum()
    fig_trans = px.bar(
        data_frame=trans_summary,
        x=trans_summary.index,
        y="amount",
        title="most repeted Expense / Income",
        color="amount",
    )

    st.plotly_chart(fig_trans)

    # . the which project have highest amount

    highest_project = transaction_project.loc[transaction_project["amount"].idxmax()]
    st.subheader("the highest project")
    st.write(f"**Project Name:** {highest_project['project_name']}")
    st.write(f"**Client ID:** {highest_project['client_id_x']}")
    st.write(f"**Budget:** ${highest_project['budget']}")


# ~/.////////// marketing sections /////////////


with marketing_sections:
    st.header("marketing analysis")

    st.subheader("marketing status info:")

    marketing_status = marketing_campaign["status"].value_counts()

    st1, st2, st3 = st.columns([0.3, 0.3, 0.3])

    with st1:
        st.metric("number of Completed", marketing_status["Completed"])

    with st2:
        st.metric("number of In Progress", marketing_status["In Progress"])

    with st3:
        st.metric("number of In Progress", marketing_status["Planned"])

    # = most channel used for marketing

    channel_fig, channel_info = st.columns([0.7, 0.3])

    channels = marketing_campaign["channel"].value_counts()

    with channel_fig:
        fig = px.bar(data_frame=channels, x=channels.index, y="count", color="count")
        st.plotly_chart(fig)

    with channel_info:

        st.header("Top 2 channels")
        email, social = st.columns([0.5, 0.5])

        with email:
            st.metric("Email", channels["Email"])

        with social:
            st.metric("Social Media", channels["Social Media"])

# ././///// tasks section ///////

with tasks_sections:

    st.header("tasks analysis")

    st.subheader("Tasks info:")

    tasks_info = tasks["status"].value_counts()
    fig = px.bar(
        data_frame=tasks_info, x=tasks_info.index, y="count", color=tasks_info.index
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns([0.3, 0.3, 0.3])

    with col1:
        st.subheader("Completed")
        st.metric("Number of completed Tasks:", tasks_info[0])

    with col2:
        st.subheader("In Progress")
        st.metric("Number of In Progress Tasks:", tasks_info[1])

    with col3:
        st.subheader("Planned")
        st.metric("Number of Planned Tasks:", tasks_info[2])
