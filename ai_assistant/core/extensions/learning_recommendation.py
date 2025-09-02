def recommend_learning_resources(topic):
    topic = topic.lower()
    resources = {
        "python": [
            "https://www.learnpython.org/",
            "https://realpython.com/",
            "https://docs.python.org/3/"
        ],
        "machine learning": [
            "https://www.coursera.org/learn/machine-learning",
            "https://developers.google.com/machine-learning/crash-course",
            "https://scikit-learn.org/"
        ],
        "cybersecurity": [
            "https://owasp.org/www-project-top-ten/",
            "https://tryhackme.com/",
            "https://www.hackthebox.com/"
        ],
        "ai": [
            "https://www.deeplearning.ai/",
            "https://cs50.harvard.edu/ai/",
            "https://towardsdatascience.com/"
        ]
    }

    for key in resources:
        if key in topic:
            return resources[key]

    return [f"No specific resources found for '{topic}', but try https://www.khanacademy.org/ or https://www.edx.org/"]
