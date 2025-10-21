<template>
  <div class="news-page">
    <h1>News</h1>

    <div v-if="loading" class="loading">Loading news...</div>
    <div v-else-if="news.length === 0" class="no-news">No news available.</div>

    <div v-else class="news-list">
      <div v-for="item in news" :key="item.id" class="news-card">
        <!-- عکس خبر یا placeholder -->
        <div class="image-container">
          <img :src="item.image_url !== 'string' ? item.image_url : 'https://via.placeholder.com/200x150?text=No+Image'" alt="News image" />
        </div>

        <!-- محتوای خبر -->
        <div class="news-content">
          <h2>{{ item.title }}</h2>
          <p>{{ item.summary }}</p>
          <small>Published at: {{ formatDate(item.published_at) }}</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  name: "NewsList",
  setup() {
    const news = ref([]);
    const loading = ref(true);

    // گرفتن اخبار از backend
    const fetchNews = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/news/public?skip=0&limit=10");
        const data = await res.json();
        news.value = data;
      } catch (err) {
        console.error("Failed to fetch news:", err);
      } finally {
        loading.value = false;
      }
    };

    // فرمت تاریخ
    const formatDate = (dateStr) => {
      if (!dateStr) return "";
      return new Date(dateStr).toLocaleString();
    };

    // بررسی URL تصویر، اگر خالی بود عکس placeholder بده
    const validImage = (url) => {
      if (!url || url === "string") {
        return "https://via.placeholder.com/200x150?text=No+Image";
      }
      return url;
    };

    onMounted(() => {
      fetchNews();
    });

    return { news, loading, formatDate, validImage };
  }
};
</script>

<style scoped>
.news-page {
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.loading,
.no-news {
  text-align: center;
  font-size: 18px;
  color: #666;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.news-card {
  display: flex;
  gap: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.news-card:hover {
  transform: scale(1.02);
}

.image-container {
  flex-shrink: 0;
  width: 200px;
  height: 150px;
  overflow: hidden;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.news-content {
  padding: 15px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.news-content h2 {
  margin: 0 0 10px 0;
  font-size: 20px;
  color: #333;
}

.news-content p {
  margin: 0 0 10px 0;
  color: #555;
}

.news-content small {
  color: #999;
}
</style>
