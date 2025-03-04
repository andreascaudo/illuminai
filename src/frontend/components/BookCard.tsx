import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { FiBook, FiFile, FiFileText } from 'react-icons/fi';

interface BookCardProps {
  id: number;
  title: string;
  author: string | null;
  format: string;
  coverUrl: string | null;
}

const BookCard: React.FC<BookCardProps> = ({ id, title, author, format, coverUrl }) => {
  // Format icon based on book type
  const FormatIcon = () => {
    switch (format) {
      case 'epub':
        return <FiBook className="w-6 h-6 text-primary-500" />;
      case 'pdf':
        return <FiFile className="w-6 h-6 text-red-500" />;
      case 'txt':
        return <FiFileText className="w-6 h-6 text-gray-500" />;
      default:
        return <FiBook className="w-6 h-6 text-primary-500" />;
    }
  };

  return (
    <Link href={`/read/${id}`} className="book-card">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transition-shadow hover:shadow-lg">
        <div className="relative aspect-[2/3] bg-gray-100 dark:bg-gray-700">
          {coverUrl ? (
            <Image
              src={coverUrl}
              alt={title}
              fill
              className="object-cover"
            />
          ) : (
            <div className="absolute inset-0 flex flex-col items-center justify-center p-4 text-center">
              <FormatIcon />
              <div className="mt-2 font-medium text-gray-900 dark:text-white line-clamp-3">
                {title}
              </div>
            </div>
          )}
        </div>
        <div className="p-4">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white line-clamp-2">
            {title}
          </h3>
          {author && (
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {author}
            </p>
          )}
          <div className="flex items-center mt-2 text-sm text-gray-500 dark:text-gray-400">
            <FormatIcon />
            <span className="ml-1 uppercase">{format}</span>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default BookCard;