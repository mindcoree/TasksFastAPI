'use client';
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';

interface Post {
  id: number;
  title: string;
  content: string;
  author: string;
  date: string;
  category: string;
}

export default function Home() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  useEffect(() => {
    fetch('http://localhost:8000/posts/')
      .then(response => response.json())
      .then(data => {
        setPosts(data);
        // Extract unique categories
        const uniqueCategories = ['All', ...new Set(data.map((post: Post) => post.category))];
        setCategories(uniqueCategories);
      });
  }, []);

  const filteredPosts = selectedCategory === 'All'
    ? posts
    : posts.filter(post => post.category === selectedCategory);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Blog Posts</h1>

      {/* Category Filter */}
      <div className="mb-4">
        <label htmlFor="category" className="mr-2">Filter by Category:</label>
        <select
          id="category"
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="border rounded p-1"
        >
          {categories.map(category => (
            <option key={category} value={category}>{category}</option>
          ))}
        </select>
      </div>

      {/* Posts List */}
      {filteredPosts.map(post => (
        <div key={post.id} className="mb-4 p-4 border rounded">
          <Link href={`/posts/${post.id}`}>
            <h2 className="text-xl font-semibold">{post.title}</h2>
          </Link>
          <p className="text-gray-600">By {post.author} on {post.date}</p>
          <ReactMarkdown className="prose">{post.content}</ReactMarkdown>
        </div>
      ))}
    </div>
  );
}