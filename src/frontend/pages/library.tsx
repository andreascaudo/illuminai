import React, { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import BookCard from '@/components/BookCard';
import axios from 'axios';
import { toast } from 'react-toastify';
import { FiSearch, FiPlus } from 'react-icons/fi';
import Link from 'next/link';

interface Book {
  id: number;
  title: string;
  author: string | null;
  format: string;
  cover_image_url: string | null;
}

const Library: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await axios.get('/api/books');
        setBooks(response.data);
      } catch (error) {
        console.error('Error fetching books:', error);
        toast.error('Failed to load your library');
      } finally {
        setLoading(false);
      }
    };

    fetchBooks();
  }, []);

  // Filter books based on search query
  const filteredBooks = books.filter(
    (book) =>
      book.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (book.author && book.author.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <Layout title="My Library - Illuminai" requireAuth>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4 sm:mb-0">My Library</h1>
          <div className="flex flex-col sm:flex-row w-full sm:w-auto space-y-4 sm:space-y-0 sm:space-x-4">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <FiSearch className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search books..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md leading-5 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
            </div>
            <Link
              href="/upload"
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <FiPlus className="-ml-1 mr-2 h-5 w-5" />
              Upload Book
            </Link>
          </div>
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <div className="w-12 h-12 border-t-4 border-primary-500 border-solid rounded-full animate-spin"></div>
          </div>
        ) : books.length === 0 ? (
          <div className="text-center py-20">
            <h2 className="text-xl font-medium text-gray-900 dark:text-white mb-4">Your library is empty</h2>
            <p className="text-gray-500 dark:text-gray-400 mb-8">Upload your first book to get started</p>
            <Link
              href="/upload"
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <FiPlus className="-ml-1 mr-2 h-5 w-5" />
              Upload Book
            </Link>
          </div>
        ) : filteredBooks.length === 0 ? (
          <div className="text-center py-20">
            <h2 className="text-xl font-medium text-gray-900 dark:text-white mb-4">No books found</h2>
            <p className="text-gray-500 dark:text-gray-400">
              No books match your search &quot;{searchQuery}&quot;
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6">
            {filteredBooks.map((book) => (
              <BookCard
                key={book.id}
                id={book.id}
                title={book.title}
                author={book.author}
                format={book.format}
                coverUrl={book.cover_image_url}
              />
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Library;