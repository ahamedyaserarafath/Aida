#**Introduction**

AIDA (Artificially Incident Assistant),  aims to address the common challenge faced by SaaS applications - understanding the root cause of incidents and service outages that can impact their performance. In this article, we will delve into the problem statement, solution, tools, and architecture of AIDA using GCP.


#**Problem Statement**

SaaS applications often encounter issues that impact their performance, but identifying the root cause can be a time-consuming task. While the focus is typically on the application itself, external infrastructure dependencies can also contribute to these incidents. For example, if a SaaS application relies on Cloud Storage, Cloud SQL, and GKE (Google Kubernetes Engine), network latency affecting the Cloud SQL Persistent Disk can slow down the entire application.


#Solution: AIDA - Artificially Incident Assistant

AIDA is an innovative solution that aims to streamline incident management and provide customized notifications to customers whenever an incident or service outage occurs on their registered applications. By leveraging the power of GCP and its various services, AIDA helps businesses gain deeper insights into incidents, enabling them to take proactive measures and minimize downtime.


#Tools and GCP Services Used

AIDA utilized various tools and services offered by GCP to develop this impactful solution. These tools and services include:



Cloud Pub/Sub: A messaging service that enables the integration of various components within the system.

Cloud Scheduler: A fully managed cron job service that allows the scheduling of recurring tasks.

Cloud Function: A serverless compute platform that lets you run code in response to events.

Cloud SQL: A fully managed relational database service for MySQL, PostgreSQL, and SQL Server.

Cloud AppEngine: A fully managed platform for deploying and scaling web applications.


Product Architecture: AIDA

AIDA encompasses the core logic of the incident management system. It is designed to handle incidents effectively and provide timely notifications to registered users. Let's take a closer look at the architecture of AIDA.
![image](https://github.com/ahamedyaserarafath/Aida/assets/4734859/e99c7d84-d04a-43e7-95a9-65af91533ef8)


AIDA Flow Chart

The flow chart below illustrates the high-level process flow of AIDA:


![image](https://github.com/ahamedyaserarafath/Aida/assets/4734859/33777cdd-1e9f-4ed4-91e0-33e6998ca954)


Full Demo Video

To get a comprehensive understanding of AIDA in action, you can watch the full demo video here.

https://www.youtube.com/watch?v=tifw8JLJTDs


Conclusion

AIDA leverages the power of GCP to streamline incident management and provide customized notifications to registered users. With its innovative architecture and integration with various GCP services, AIDA empowers businesses to proactively address incidents and minimize downtime. By utilizing tools like Cloud Pub/Sub, Cloud Scheduler, Cloud Function, and Cloud SQL, AIDA offers a robust incident management system that can greatly benefit SaaS applications and their users.

