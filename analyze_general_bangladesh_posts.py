import pandas as pd
from textblob import TextBlob
from collections import Counter
import os

print("=" * 100)
print("SENTIMENT ANALYSIS - GENERAL BANGLADESH POSTS (Non-Dhaka Focused)")
print("=" * 100)
print()

# Load original data
df_all = pd.read_csv("advanced_sentiment_analysis/05_posts_with_advanced_analysis.csv")
df_dhaka = pd.read_csv("advanced_sentiment_analysis/05_posts_dhaka_only.csv")

# Get non-Dhaka posts
dhaka_titles = set(df_dhaka['title'].values)
df_non_dhaka = df_all[~df_all['title'].isin(dhaka_titles)].copy()

print(f"📊 Dataset: {len(df_non_dhaka)} posts NOT specifically about Dhaka")
print(f"From r/bangladesh and r/dhaka subreddits")
print(f"Date Range: Last 3 months")
print()

# ===== SENTIMENT ANALYSIS =====
def advanced_sentiment(text):
    """Calculate sentiment with polarity and subjectivity"""
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.1:
        sentiment = 'positive'
    elif polarity < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return polarity, subjectivity, sentiment

# ===== EMOTION DETECTION =====
emotion_keywords = {
    'joy': ['good', 'great', 'love', 'happy', 'excellent', 'amazing', 'awesome', 'wonderful', 
            'best', 'beautiful', 'perfect', 'nice', 'fantastic', 'brilliant', 'lovely', 'enjoyed'],
    'anger': ['angry', 'furious', 'hate', 'bad', 'terrible', 'awful', 'horrible', 'disgusting',
              'frustrated', 'annoyed', 'upset', 'irritated', 'outrageous', 'worst', 'stupid', 'dumb'],
    'sadness': ['sad', 'depressed', 'unhappy', 'down', 'miserable', 'sorrowful', 'hurt', 
                'broken', 'heartbroken', 'cry', 'suffering', 'struggle', 'difficult', 'hard'],
    'fear': ['afraid', 'scared', 'worried', 'anxious', 'nervous', 'panic', 'fear', 'terrified',
             'concerned', 'uncertain', 'risky', 'danger', 'dangerous', 'threat'],
    'trust': ['trust', 'reliable', 'recommend', 'believe', 'confident', 'honest', 'faithful',
              'loyal', 'sincere', 'genuine', 'authentic', 'credible', 'reputable'],
    'surprise': ['surprise', 'amazing', 'shocking', 'unexpected', 'wow', 'astonished', 'stunned',
                 'amazed', 'surprising', 'interesting', 'curious', 'intrigued']
}

def detect_emotion(text):
    """Detect emotions in text"""
    text_lower = str(text).lower()
    emotions_found = {}
    
    for emotion, keywords in emotion_keywords.items():
        count = sum(1 for keyword in keywords if keyword in text_lower)
        if count > 0:
            emotions_found[emotion] = count
    
    if emotions_found:
        return max(emotions_found, key=emotions_found.get)
    return 'neutral'

# ===== TOPIC CATEGORIZATION =====
topic_keywords = {
    'Food/Dining': ['food', 'restaurant', 'eat', 'cafe', 'breakfast', 'lunch', 'dinner', 'soup', 'biryani', 'pizza', 'burger', 'tea'],
    'Healthcare/Medical': ['doctor', 'hospital', 'dermatologist', 'surgery', 'medicine', 'health', 'patient', 'disease', 'treatment', 'psychiatrist', 'dental', 'baby'],
    'Housing/Real Estate': ['flat', 'apartment', 'rent', 'house', 'property', 'building', 'landlord', 'tenant', 'lease'],
    'Technology/Gadgets': ['phone', 'laptop', 'computer', 'gadget', 'software', 'app', 'tech', 'keyboard', 'repair', 'gaming', 'internet'],
    'Shopping/Commerce': ['buy', 'shop', 'sell', 'store', 'price', 'cost', 'product', 'clothes', 'shoes', 'online', 'market', 'scam'],
    'Education/Career': ['job', 'internship', 'university', 'college', 'school', 'exam', 'study', 'course', 'learning', 'work', 'career', 'abroad'],
    'Travel/Transportation': ['flight', 'travel', 'trip', 'tour', 'hotel', 'transport', 'road', 'traffic', 'taxi', 'bus', 'metro', 'visa'],
    'Sports/Recreation': ['sports', 'gym', 'fitness', 'football', 'cricket', 'badminton', 'swimming', 'climbing', 'game', 'exercise'],
    'Entertainment': ['movie', 'concert', 'music', 'entertainment', 'show', 'event', 'festival', 'comedy', 'film', 'anime'],
    'Relationships/Social': ['relationship', 'dating', 'marriage', 'wedding', 'love', 'couple', 'friend', 'family', 'social'],
    'Politics/Government': ['politics', 'government', 'election', 'minister', 'parliament', 'policy', 'law', 'party', 'president', 'police'],
    'Services/Professional': ['lawyer', 'accountant', 'tax', 'legal', 'repair', 'service', 'professional', 'consultant'],
}

def categorize_topics(text):
    """Categorize topics from text"""
    text_lower = str(text).lower()
    topics = []
    
    for topic, keywords in topic_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            topics.append(topic)
    
    if not topics:
        topics.append('General/Miscellaneous')
    
    return ', '.join(topics)

# Apply analysis
print("🔍 Analyzing sentiment...")
df_non_dhaka['polarity'] = 0.0
df_non_dhaka['subjectivity'] = 0.0
df_non_dhaka['sentiment'] = ''
df_non_dhaka['emotion'] = ''
df_non_dhaka['topics'] = ''

for idx, row in df_non_dhaka.iterrows():
    if (idx - df_non_dhaka.index[0]) % 30 == 0:
        print(f"   Processing... {idx - df_non_dhaka.index[0]}/{len(df_non_dhaka)}")
    
    title = str(row['title'])
    polarity, subjectivity, sentiment = advanced_sentiment(title)
    emotion = detect_emotion(title)
    topics = categorize_topics(title)
    
    df_non_dhaka.at[idx, 'polarity'] = polarity
    df_non_dhaka.at[idx, 'subjectivity'] = subjectivity
    df_non_dhaka.at[idx, 'sentiment'] = sentiment
    df_non_dhaka.at[idx, 'emotion'] = emotion
    df_non_dhaka.at[idx, 'topics'] = topics

print(f"✓ Analysis complete!")
print()

# ===== STATISTICS =====
print("=" * 100)
print("📊 SENTIMENT STATISTICS - NON-DHAKA POSTS")
print("=" * 100)

sentiment_counts = df_non_dhaka['sentiment'].value_counts()
print("\nSentiment Distribution:")
for sentiment, count in sentiment_counts.items():
    pct = (count / len(df_non_dhaka)) * 100
    print(f"  {sentiment.capitalize()}: {count} ({pct:.1f}%)")

print(f"\nAverage Polarity: {df_non_dhaka['polarity'].mean():.3f}")
print(f"Average Subjectivity: {df_non_dhaka['subjectivity'].mean():.3f}")

print()

# ===== EMOTION DISTRIBUTION =====
emotion_counts = df_non_dhaka['emotion'].value_counts()
print("=" * 100)
print("😊 EMOTION DISTRIBUTION - NON-DHAKA POSTS")
print("=" * 100)

for emotion, count in emotion_counts.items():
    pct = (count / len(df_non_dhaka)) * 100
    print(f"  {emotion.capitalize()}: {count} ({pct:.1f}%)")

print()

# ===== TOPIC ANALYSIS =====
print("=" * 100)
print("🏷️  TOP TOPICS DISCUSSED - NON-DHAKA POSTS")
print("=" * 100)

all_topics = []
for topics_str in df_non_dhaka['topics']:
    topics = [t.strip() for t in str(topics_str).split(',')]
    all_topics.extend(topics)

topic_counter = Counter(all_topics)
print()
for idx, (topic, count) in enumerate(topic_counter.most_common(15), 1):
    pct = (count / len(df_non_dhaka)) * 100
    print(f"{idx}. {topic}: {count} posts ({pct:.1f}%)")

print()

# ===== TOPIC SENTIMENT ANALYSIS =====
print("=" * 100)
print("💬 SENTIMENT BY TOPIC - NON-DHAKA POSTS")
print("=" * 100)

topic_sentiment = []
for topic in list(dict(topic_counter.most_common(10)).keys()):
    topic_df = df_non_dhaka[df_non_dhaka['topics'].str.contains(topic, na=False)]
    if len(topic_df) > 0:
        pos = (topic_df['sentiment'] == 'positive').sum()
        neg = (topic_df['sentiment'] == 'negative').sum()
        neu = (topic_df['sentiment'] == 'neutral').sum()
        avg_pol = topic_df['polarity'].mean()
        
        print(f"\n{topic}")
        print(f"  Posts: {len(topic_df)}")
        print(f"  Positive: {pos} ({pos/len(topic_df)*100:.0f}%)")
        print(f"  Negative: {neg} ({neg/len(topic_df)*100:.0f}%)")
        print(f"  Neutral: {neu} ({neu/len(topic_df)*100:.0f}%)")
        print(f"  Avg Polarity: {avg_pol:.3f}")
        print(f"  Vibe: {'😊 Happy' if avg_pol > 0.1 else '😐 Neutral' if avg_pol > -0.1 else '😞 Critical'}")

print()

# ===== COMPARISON: DHAKA vs NON-DHAKA =====
print("=" * 100)
print("🔄 COMPARISON: DHAKA-FOCUSED vs GENERAL BANGLADESH POSTS")
print("=" * 100)

dhaka_sentiment = df_dhaka['sentiment'].value_counts()
non_dhaka_sentiment = df_non_dhaka['sentiment'].value_counts()

print(f"\n{'Metric':<25} {f'Dhaka ({len(df_dhaka)})':<20} {f'General BD ({len(df_non_dhaka)})':<20}")
print("-" * 65)
print(f"{'Positive':<25} {dhaka_sentiment.get('positive', 0):>6} ({dhaka_sentiment.get('positive', 0)/len(df_dhaka)*100:>5.1f}%) {non_dhaka_sentiment.get('positive', 0):>6} ({non_dhaka_sentiment.get('positive', 0)/len(df_non_dhaka)*100:>5.1f}%)")
print(f"{'Negative':<25} {dhaka_sentiment.get('negative', 0):>6} ({dhaka_sentiment.get('negative', 0)/len(df_dhaka)*100:>5.1f}%) {non_dhaka_sentiment.get('negative', 0):>6} ({non_dhaka_sentiment.get('negative', 0)/len(df_non_dhaka)*100:>5.1f}%)")
print(f"{'Neutral':<25} {dhaka_sentiment.get('neutral', 0):>6} ({dhaka_sentiment.get('neutral', 0)/len(df_dhaka)*100:>5.1f}%) {non_dhaka_sentiment.get('neutral', 0):>6} ({non_dhaka_sentiment.get('neutral', 0)/len(df_non_dhaka)*100:>5.1f}%)")
print(f"{'Avg Polarity':<25} {df_dhaka['polarity'].mean():>27.3f} {df_non_dhaka['polarity'].mean():>27.3f}")
print(f"{'Avg Upvotes':<25} {df_dhaka['upvotes'].mean():>27.1f} {df_non_dhaka['upvotes'].mean():>27.1f}")

print()

# ===== TOP POSTS =====
print("=" * 100)
print("✨ TOP 10 MOST POSITIVE POSTS - GENERAL BANGLADESH")
print("=" * 100)

top_positive = df_non_dhaka.nlargest(10, 'polarity')[['title', 'subreddit', 'polarity', 'emotion', 'upvotes']]
print()
for idx, (_, row) in enumerate(top_positive.iterrows(), 1):
    print(f"{idx}. [{row['subreddit']}] {row['title'][:70]}")
    print(f"   Polarity: {row['polarity']:.3f} | Emotion: {row['emotion']} | Upvotes: {row['upvotes']}")

print()

print("=" * 100)
print("⚠️  TOP 10 MOST NEGATIVE POSTS - GENERAL BANGLADESH")
print("=" * 100)

top_negative = df_non_dhaka.nsmallest(10, 'polarity')[['title', 'subreddit', 'polarity', 'emotion', 'upvotes']]
print()
for idx, (_, row) in enumerate(top_negative.iterrows(), 1):
    print(f"{idx}. [{row['subreddit']}] {row['title'][:70]}")
    print(f"   Polarity: {row['polarity']:.3f} | Emotion: {row['emotion']} | Upvotes: {row['upvotes']}")

print()

# ===== SAVE RESULTS =====
output_dir = "general_bangladesh_analysis"
os.makedirs(output_dir, exist_ok=True)

# Full analysis
df_non_dhaka.to_csv(f"{output_dir}/01_full_analysis.csv", index=False, encoding='utf-8')

# Most positive
df_non_dhaka.nlargest(15, 'polarity')[['title', 'subreddit', 'polarity', 'emotion', 'topics', 'upvotes', 'comments']].to_csv(
    f"{output_dir}/02_most_positive_posts.csv", index=False, encoding='utf-8'
)

# Most negative
df_non_dhaka.nsmallest(15, 'polarity')[['title', 'subreddit', 'polarity', 'emotion', 'topics', 'upvotes', 'comments']].to_csv(
    f"{output_dir}/03_most_negative_posts.csv", index=False, encoding='utf-8'
)

# Topic analysis
topic_analysis = []
for topic in list(dict(topic_counter.most_common(12)).keys()):
    topic_df = df_non_dhaka[df_non_dhaka['topics'].str.contains(topic, na=False)]
    if len(topic_df) > 0:
        topic_analysis.append({
            'topic': topic,
            'posts': len(topic_df),
            'positive': (topic_df['sentiment'] == 'positive').sum(),
            'negative': (topic_df['sentiment'] == 'negative').sum(),
            'neutral': (topic_df['sentiment'] == 'neutral').sum(),
            'avg_polarity': topic_df['polarity'].mean(),
            'avg_upvotes': topic_df['upvotes'].mean(),
            'total_upvotes': topic_df['upvotes'].sum()
        })

pd.DataFrame(topic_analysis).to_csv(f"{output_dir}/04_topic_sentiment_analysis.csv", index=False, encoding='utf-8')

# Subreddit comparison
subreddit_analysis = []
for subreddit in df_non_dhaka['subreddit'].unique():
    sub_df = df_non_dhaka[df_non_dhaka['subreddit'] == subreddit]
    subreddit_analysis.append({
        'subreddit': subreddit,
        'posts': len(sub_df),
        'positive': (sub_df['sentiment'] == 'positive').sum(),
        'negative': (sub_df['sentiment'] == 'negative').sum(),
        'neutral': (sub_df['sentiment'] == 'neutral').sum(),
        'avg_polarity': sub_df['polarity'].mean(),
        'avg_upvotes': sub_df['upvotes'].mean()
    })

pd.DataFrame(subreddit_analysis).to_csv(f"{output_dir}/05_subreddit_comparison.csv", index=False, encoding='utf-8')

# Combined comparison
combined_comparison = pd.DataFrame({
    'Analysis_Type': ['Dhaka-Focused Posts', 'General Bangladesh Posts', 'All Posts'],
    'Total_Posts': [len(df_dhaka), len(df_non_dhaka), len(df_all)],
    'Positive_%': [
        (df_dhaka['sentiment'] == 'positive').sum() / len(df_dhaka) * 100,
        (df_non_dhaka['sentiment'] == 'positive').sum() / len(df_non_dhaka) * 100,
        (df_all['sentiment'] == 'positive').sum() / len(df_all) * 100
    ],
    'Negative_%': [
        (df_dhaka['sentiment'] == 'negative').sum() / len(df_dhaka) * 100,
        (df_non_dhaka['sentiment'] == 'negative').sum() / len(df_non_dhaka) * 100,
        (df_all['sentiment'] == 'negative').sum() / len(df_all) * 100
    ],
    'Neutral_%': [
        (df_dhaka['sentiment'] == 'neutral').sum() / len(df_dhaka) * 100,
        (df_non_dhaka['sentiment'] == 'neutral').sum() / len(df_non_dhaka) * 100,
        (df_all['sentiment'] == 'neutral').sum() / len(df_all) * 100
    ],
    'Avg_Polarity': [df_dhaka['polarity'].mean(), df_non_dhaka['polarity'].mean(), df_all['polarity'].mean()],
    'Avg_Upvotes': [df_dhaka['upvotes'].mean(), df_non_dhaka['upvotes'].mean(), df_all['upvotes'].mean()]
})

combined_comparison.to_csv(f"{output_dir}/06_comprehensive_comparison.csv", index=False, encoding='utf-8')

print("=" * 100)
print("✓ FILES SAVED")
print("=" * 100)
print(f"📁 Output Directory: {output_dir}/")
print(f"  • 01_full_analysis.csv - Complete data with all metrics")
print(f"  • 02_most_positive_posts.csv - Top 15 positive posts")
print(f"  • 03_most_negative_posts.csv - Top 15 negative posts")
print(f"  • 04_topic_sentiment_analysis.csv - Sentiment by topic")
print(f"  • 05_subreddit_comparison.csv - r/dhaka vs r/bangladesh")
print(f"  • 06_comprehensive_comparison.csv - Dhaka vs General vs All Posts")
print()

# Final summary
print("=" * 100)
print("📋 KEY INSIGHTS")
print("=" * 100)

print(f"""
DHAKA-FOCUSED POSTS ({len(df_dhaka)}):
  • {(df_dhaka['sentiment'] == 'neutral').sum() / len(df_dhaka) * 100:.1f}% neutral (asking for help)
  • {(df_dhaka['sentiment'] == 'positive').sum() / len(df_dhaka) * 100:.1f}% positive - when finding good services
  • {(df_dhaka['sentiment'] == 'negative').sum() / len(df_dhaka) * 100:.1f}% negative

GENERAL BANGLADESH POSTS ({len(df_non_dhaka)}):
  • More critical/political ({(df_non_dhaka['sentiment'] == 'negative').sum() / len(df_non_dhaka) * 100:.1f}% negative)
  • {(df_non_dhaka['sentiment'] == 'positive').sum() / len(df_non_dhaka) * 100:.1f}% positive
  • {(df_non_dhaka['sentiment'] == 'neutral').sum() / len(df_non_dhaka) * 100:.1f}% neutral

MAIN DIFFERENCE:
  ✓ Dhaka posts = "Where can I find X?" (practical)
  ✗ General BD posts = "This is wrong!" (critical/political)

OVERALL DATASET ({len(df_all)} posts):
  • {(df_all['sentiment'] == 'positive').sum()} positive ({(df_all['sentiment'] == 'positive').sum() / len(df_all) * 100:.1f}%)
  • {(df_all['sentiment'] == 'neutral').sum()} neutral ({(df_all['sentiment'] == 'neutral').sum() / len(df_all) * 100:.1f}%)
  • {(df_all['sentiment'] == 'negative').sum()} negative ({(df_all['sentiment'] == 'negative').sum() / len(df_all) * 100:.1f}%)
  • Avg polarity: {df_all['polarity'].mean():.3f}
""")
