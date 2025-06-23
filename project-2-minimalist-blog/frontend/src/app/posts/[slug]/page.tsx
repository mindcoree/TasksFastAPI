'use client';
import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import ReactMarkdown from 'react-markdown';

interface Post {
  id: number;
  title: string;
  content: string;
  author: string;
  date: string;
  category: string;
}

export default function PostPage() {
  const [post, setPost] = useState<Post | null>(null);
  const params = useParams();
  const postId = params.id;

  useEffect(() => {
    fetch(`http://localhost:8000/posts/${postId}`)
      .then(response => response.json())
      .then(data => setPost(data));
  }, [postId]);

  if (!post) return <div>Loading...</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">{post.title}</h1>
      <p className="text-gray-600 mb-4">By {post.author} on {post.date} | Category: {post.category}</p>
      <ReactMarkdown className="prose">{post.content}</ReactMarkdown>
    </div>
  );
}