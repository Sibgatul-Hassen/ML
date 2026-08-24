import pandas as pd
import numpy as np
from collections import Counter
import re

print("=" * 100)
print("WHAT ARE DHAKA PEOPLE TALKING ABOUT? - COMPREHENSIVE ANALYSIS")
print("=" * 100)
print()

# Load data
df = pd.read_csv("advanced_sentiment_analysis/05_posts_with_advanced_analysis.csv")

print("📊 DATASET OVERVIEW")
print("-" * 100)
print(f"Total Posts Analyzed: {len(df)}")
print(f"From Subreddits: r/bangladesh, r/dhaka")
print(f"Date Range: Last 3 months")
print()

# ===== 1. TOPIC BREAKDOWN =====
print("🏷️  MAIN TOPICS PEOPLE ARE DISCUSSING")
print("-" * 100)

topic_map = {
    'Housing/Real Estate': {
        'posts': 0,
        'examples': [],
        'concerns': []
    },
    'Technology/Gadgets': {
        'posts': 0,
        'examples': [],
        'concerns': []
    },
    'Education/Career': {
        'posts': 0,
        'examples': [],
        'concerns': []
    },
    'Travel/Transportation': {
        'posts': 0,
        'examples': [],
        'concerns': []
    },
    'Relationships/Social': {
        'posts': 0,
        'examples': [],
        'concerns': []
    },
    'Food/Dining': {
        'posts': 0,
        'examples': [],
        'concerns': []
    },
    'Shopping/Commerce': {
        'posts': 0,
        'examples': [],
        'concerns': []
    },
    'Infrastructure/Urban': {
        'posts': 0,
        'examples': [],
        'concerns': []
    },
    'Health/Medical': {
        'posts': 0,
        'examples': [],
        'concerns': []
    },
    'Politics/Government': {
        'posts': 0,
        'examples': [],
        'concerns': []
    },
}

# Count and collect examples
for idx, row in df.iterrows():
    topics_str = str(row['topics'])
    title = str(row['title'])
    
    for topic in topic_map.keys():
        if topic in topics_str:
            topic_map[topic]['posts'] += 1
            if len(topic_map[topic]['examples']) < 3:
                topic_map[topic]['examples'].append(title[:70])

# Sort by number of posts
sorted_topics = sorted(topic_map.items(), key=lambda x: x[1]['posts'], reverse=True)

for idx, (topic, data) in enumerate(sorted_topics, 1):
    if data['posts'] > 0:
        pct = (data['posts'] / len(df)) * 100
        print(f"\n{idx}. {topic}")
        print(f"   Posts: {data['posts']} ({pct:.1f}%)")
        print(f"   Sample Discussions:")
        for ex in data['examples']:
            print(f"     • {ex}...")

print()

# ===== 2. HOUSING/REAL ESTATE IN DETAIL =====
housing_pct = topic_map['Housing/Real Estate']['posts'] / len(df) * 100
print("=" * 100)
print(f"🏠 HOUSING & REAL ESTATE ({housing_pct:.0f}% of discussions)")
print("-" * 100)

housing_df = df[df['topics'].str.contains('Housing/Real Estate', na=False)]
housing_titles = housing_df['title'].str.lower()

housing_keywords = {
    'Finding/Looking for apartments': ['looking', 'find', 'search', 'rent', 'apartment'],
    'Pricing/Affordability': ['price', 'cost', 'expensive', 'cheap', 'afford', 'budget'],
    'Neighborhoods/Areas': ['gulshan', 'banani', 'dhanmondi', 'dhaka', 'area', 'location'],
    'Landlord/Tenant Issues': ['landlord', 'tenant', 'lease', 'deposit', 'agreement'],
    'Property Quality': ['flat', 'building', 'quality', 'condition', 'maintenance'],
    'Recommendations/Suggestions': ['suggestion', 'recommend', 'best', 'where to'],
}

print("\nTop Housing Concerns:")
for concern, keywords in housing_keywords.items():
    count = 0
    for keyword in keywords:
        count += (housing_titles.str.contains(keyword)).sum()
    if count > 0:
        print(f"  • {concern}: {count} posts")

print()

# ===== 3. TECHNOLOGY/GADGETS IN DETAIL =====
tech_pct = topic_map['Technology/Gadgets']['posts'] / len(df) * 100
print("=" * 100)
print(f"📱 TECHNOLOGY & GADGETS ({tech_pct:.0f}% of discussions)")
print("-" * 100)

tech_df = df[df['topics'].str.contains('Technology/Gadgets', na=False)]
tech_titles = tech_df['title'].str.lower()

tech_keywords = {
    'Phones/Smartphones': ['phone', 'iphone', 'android', 'samsung', 'smartphone'],
    'Laptops/Computers': ['laptop', 'computer', 'pc', 'dell', 'hp'],
    'Internet/Connectivity': ['internet', 'wifi', 'speed', 'connection', 'isp'],
    'Gaming': ['gaming', 'game', 'ps5', 'console', 'steam'],
    'Software/Apps': ['app', 'software', 'code', 'programming', 'system'],
    'Buying/Shopping': ['buy', 'shop', 'price', 'where to buy', 'cost'],
}

print("\nTop Tech Discussions:")
for concern, keywords in tech_keywords.items():
    count = 0
    for keyword in keywords:
        count += (tech_titles.str.contains(keyword)).sum()
    if count > 0:
        print(f"  • {concern}: {count} posts")

print()

# ===== 4. EDUCATION/CAREER IN DETAIL =====
edu_pct = topic_map['Education/Career']['posts'] / len(df) * 100
print("=" * 100)
print(f"🎓 EDUCATION & CAREER ({edu_pct:.0f}% of discussions)")
print("-" * 100)

edu_df = df[df['topics'].str.contains('Education/Career', na=False)]
edu_titles = edu_df['title'].str.lower()

edu_keywords = {
    'University/Higher Education': ['university', 'college', 'admission', 'undergraduate'],
    'Exams (HSC/SSC)': ['hsc', 'ssc', 'exam', 'result', 'score'],
    'Job Search': ['job', 'employment', 'interview', 'recruitment', 'hiring'],
    'Career Advice': ['career', 'advice', 'path', 'choice', 'future'],
    'Study Tips': ['study', 'prepare', 'learning', 'course', 'tuition'],
    'Skill Development': ['skill', 'programming', 'coding', 'training', 'course'],
}

print("\nTop Education/Career Topics:")
for concern, keywords in edu_keywords.items():
    count = 0
    for keyword in keywords:
        count += (edu_titles.str.contains(keyword)).sum()
    if count > 0:
        print(f"  • {concern}: {count} posts")

print()

# ===== 5. SENTIMENT BY MAJOR TOPICS =====
print("=" * 100)
print("💬 WHAT'S THE OVERALL SENTIMENT ABOUT EACH TOPIC?")
print("-" * 100)

topic_sentiment = []
for topic in ['Housing/Real Estate', 'Technology/Gadgets', 'Education/Career', 'Food/Dining', 'Relationships/Social']:
    topic_df = df[df['topics'].str.contains(topic, na=False)]
    if len(topic_df) > 0:
        pos = (topic_df['sentiment'] == 'positive').sum()
        neg = (topic_df['sentiment'] == 'negative').sum()
        neu = (topic_df['sentiment'] == 'neutral').sum()
        avg_pol = topic_df['polarity'].mean()
        
        topic_sentiment.append({
            'topic': topic,
            'posts': len(topic_df),
            'positive': f"{pos} ({pos/len(topic_df)*100:.0f}%)",
            'negative': f"{neg} ({neg/len(topic_df)*100:.0f}%)",
            'neutral': f"{neu} ({neu/len(topic_df)*100:.0f}%)",
            'avg_polarity': f"{avg_pol:.3f}",
            'sentiment_vibe': '😊 Happy' if avg_pol > 0.1 else '😐 Neutral' if avg_pol > -0.1 else '😞 Critical'
        })

sentiment_df = pd.DataFrame(topic_sentiment)
print(sentiment_df.to_string(index=False))

print()

# ===== 6. MOST DISCUSSED PROBLEMS =====
print("=" * 100)
print("⚠️  TOP PROBLEMS PEOPLE ARE COMPLAINING ABOUT")
print("-" * 100)

# Find negative posts
negative_df = df[df['sentiment'] == 'negative'].sort_values('upvotes', ascending=False).head(20)

problems = Counter()
problem_examples = {}

for idx, row in negative_df.iterrows():
    title = str(row['title']).lower()
    
    if any(word in title for word in ['traffic', 'metro', 'road', 'transport', 'bus']):
        problems['Traffic & Transportation Issues'] += row['upvotes']
        problem_examples.setdefault('Traffic & Transportation Issues', []).append(row['title'][:60])
    elif any(word in title for word in ['internet', 'wifi', 'connection', 'speed']):
        problems['Internet Quality & Speed'] += row['upvotes']
        problem_examples.setdefault('Internet Quality & Speed', []).append(row['title'][:60])
    elif any(word in title for word in ['job', 'interview', 'employment', 'work']):
        problems['Job Market & Opportunities'] += row['upvotes']
        problem_examples.setdefault('Job Market & Opportunities', []).append(row['title'][:60])
    elif any(word in title for word in ['price', 'expensive', 'cost', 'afford']):
        problems['High Costs & Affordability'] += row['upvotes']
        problem_examples.setdefault('High Costs & Affordability', []).append(row['title'][:60])
    elif any(word in title for word in ['doctor', 'hospital', 'health', 'medical']):
        problems['Healthcare Challenges'] += row['upvotes']
        problem_examples.setdefault('Healthcare Challenges', []).append(row['title'][:60])
    elif any(word in title for word in ['women', 'safety', 'harassment', 'security']):
        problems['Safety & Security Concerns'] += row['upvotes']
        problem_examples.setdefault('Safety & Security Concerns', []).append(row['title'][:60])
    elif any(word in title for word in ['hsc', 'exam', 'study', 'education']):
        problems['Education System Issues'] += row['upvotes']
        problem_examples.setdefault('Education System Issues', []).append(row['title'][:60])

print("\nTop Problems (by engagement/upvotes):")
for prob, score in sorted(problems.items(), key=lambda x: x[1], reverse=True):
    print(f"\n❌ {prob}")
    print(f"   Engagement Score: {score}")
    if prob in problem_examples:
        print(f"   Examples:")
        for ex in problem_examples[prob][:2]:
            print(f"     - {ex}...")

print()

# ===== 7. WHAT PEOPLE WANT (POSITIVE SENTIMENT) =====
print("=" * 100)
print("✨ WHAT PEOPLE ARE HAPPY ABOUT & WANT MORE OF")
print("-" * 100)

positive_df = df[df['sentiment'] == 'positive'].sort_values('upvotes', ascending=False).head(20)

happiness = Counter()
happy_examples = {}

for idx, row in positive_df.iterrows():
    title = str(row['title']).lower()
    
    if any(word in title for word in ['food', 'restaurant', 'eat', 'cafe', 'meal']):
        happiness['Food & Dining'] += row['upvotes']
        happy_examples.setdefault('Food & Dining', []).append(row['title'][:60])
    elif any(word in title for word in ['relationship', 'love', 'wedding', 'dating']):
        happiness['Relationships & Romance'] += row['upvotes']
        happy_examples.setdefault('Relationships & Romance', []).append(row['title'][:60])
    elif any(word in title for word in ['travel', 'trip', 'visit', 'tour', 'vacation']):
        happiness['Travel & Tourism'] += row['upvotes']
        happy_examples.setdefault('Travel & Tourism', []).append(row['title'][:60])
    elif any(word in title for word in ['sports', 'football', 'cricket', 'match', 'game']):
        happiness['Sports & Games'] += row['upvotes']
        happy_examples.setdefault('Sports & Games', []).append(row['title'][:60])
    elif any(word in title for word in ['success', 'achieve', 'win', 'great', 'best']):
        happiness['Success Stories'] += row['upvotes']
        happy_examples.setdefault('Success Stories', []).append(row['title'][:60])

print("\nWhat Makes Dhaka People Happy (by engagement):")
for happy, score in sorted(happiness.items(), key=lambda x: x[1], reverse=True):
    print(f"\n✅ {happy}")
    print(f"   Engagement Score: {score}")
    if happy in happy_examples:
        print(f"   Examples:")
        for ex in happy_examples[happy][:2]:
            print(f"     - {ex}...")

print()

# ===== 8. QUESTION TYPES =====
print("=" * 100)
print("❓ TYPES OF QUESTIONS PEOPLE ARE ASKING")
print("-" * 100)

question_df = df[df['title'].str.contains(r'\?', regex=True)]
question_types = {
    'Recommendations/Suggestions': 0,
    'Where To Find Something': 0,
    'How To Do Something': 0,
    'Seeking Advice': 0,
    'Information/Knowledge': 0,
    'Yes/No Questions': 0,
}

for idx, row in question_df.iterrows():
    title = str(row['title']).lower()
    
    if any(word in title for word in ['recommend', 'suggest', 'best', 'good']):
        question_types['Recommendations/Suggestions'] += 1
    elif any(word in title for word in ['where', 'how to find', 'can i get']):
        question_types['Where To Find Something'] += 1
    elif any(word in title for word in ['how to', 'how do', 'how can']):
        question_types['How To Do Something'] += 1
    elif any(word in title for word in ['advice', 'suggestion', 'help', 'opinion']):
        question_types['Seeking Advice'] += 1
    elif any(word in title for word in ['what', 'which', 'is', 'can']):
        question_types['Yes/No Questions'] += 1
    else:
        question_types['Information/Knowledge'] += 1

print(f"\nTotal Questions Asked: {len(question_df)} ({len(question_df)/len(df)*100:.1f}% of all posts)\n")
for qtype, count in sorted(question_types.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"  • {qtype}: {count} questions")

print()

# ===== 9. SUMMARY =====
print("=" * 100)
print("📋 SUMMARY - WHAT DHAKA PEOPLE ARE REALLY TALKING ABOUT")
print("=" * 100)

summary_lines = ["", "TOP TOPICS BY SHARE OF POSTS:"]
for topic, data in sorted_topics:
    if data['posts'] == 0:
        continue
    pct = data['posts'] / len(df) * 100
    topic_df_all = df[df['topics'].str.contains(re.escape(topic), na=False)]
    topic_pos_pct = (topic_df_all['sentiment'] == 'positive').sum() / len(topic_df_all) * 100 if len(topic_df_all) else 0
    summary_lines.append(f"   • {topic}: {data['posts']} posts ({pct:.0f}%) — {topic_pos_pct:.0f}% positive sentiment")

if problems:
    summary_lines.append("")
    summary_lines.append("TOP PROBLEMS PEOPLE ARE COMPLAINING ABOUT (by engagement):")
    for idx, (prob, score) in enumerate(sorted(problems.items(), key=lambda x: x[1], reverse=True), 1):
        summary_lines.append(f"   {idx}. {prob} (engagement score: {score})")

if happiness:
    summary_lines.append("")
    summary_lines.append("WHAT BRINGS MOST JOY (by engagement, positive posts):")
    for idx, (happy, score) in enumerate(sorted(happiness.items(), key=lambda x: x[1], reverse=True), 1):
        summary_lines.append(f"   {idx}. {happy} (engagement score: {score})")

overall_positive_pct = (df['sentiment'] == 'positive').sum() / len(df) * 100
overall_neutral_pct = (df['sentiment'] == 'neutral').sum() / len(df) * 100
overall_negative_pct = (df['sentiment'] == 'negative').sum() / len(df) * 100

summary_lines.append("")
summary_lines.append(f"OVERALL VIBE ({len(df)} posts): {overall_positive_pct:.1f}% positive, {overall_neutral_pct:.1f}% neutral, {overall_negative_pct:.1f}% negative")

summary = "\n".join(summary_lines) + "\n"

print(summary)

# Save summary
with open("advanced_sentiment_analysis/06_what_people_are_talking_about.txt", "w", encoding='utf-8') as f:
    f.write(summary)

print("✓ Saved to: advanced_sentiment_analysis/06_what_people_are_talking_about.txt")
print("=" * 100)
