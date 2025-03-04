import React, { useState, useEffect, useRef } from 'react';
import Layout from '@/components/Layout';
import { useRouter } from 'next/router';
import axios from 'axios';
import { toast } from 'react-toastify';
import { FiArrowLeft, FiArrowRight, FiSettings, FiBookOpen } from 'react-icons/fi';
import { pdfjs } from 'react-pdf';
import { Document, Page } from 'react-pdf';
import dynamic from 'next/dynamic';

// Initialize PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.js`;

// Dynamically import the EPUB reader component
const EpubReader = dynamic(() => import('@/components/EpubReader'), {
  ssr: false,
  loading: () => (
    <div className="flex justify-center py-20">
      <div className="w-12 h-12 border-t-4 border-primary-500 border-solid rounded-full animate-spin"></div>
    </div>
  ),
});

// Define book interface
interface Book {
  id: number;
  title: string;
  author: string | null;
  description: string | null;
  format: string;
  file_path: string;
}

const ReadPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;
  const [book, setBook] = useState<Book | null>(null);
  const [loading, setLoading] = useState(true);
  const [bookUrl, setBookUrl] = useState<string | null>(null);
  
  // PDF specific state
  const [numPages, setNumPages] = useState<number | null>(null);
  const [pageNumber, setPageNumber] = useState<number>(1);
  
  // TXT specific state
  const [textContent, setTextContent] = useState<string | null>(null);
  
  // Reader settings
  const [fontSize, setFontSize] = useState<number>(16);
  const [showSettings, setShowSettings] = useState<boolean>(false);

  // Fetch book data
  useEffect(() => {
    const fetchBook = async () => {
      if (!id) return;
      
      try {
        // Fetch book details
        const response = await axios.get(`/api/books/${id}`);
        setBook(response.data);
        
        // Generate temp URL for the book file
        // In a real app, this would be a signed URL or a dedicated endpoint
        // For demo purposes, we'll just use a placeholder
        setBookUrl(`/api/books/${id}/content`);
      } catch (error) {
        console.error('Error fetching book:', error);
        toast.error('Failed to load book');
        router.push('/library');
      } finally {
        setLoading(false);
      }
    };

    fetchBook();
  }, [id, router]);

  // PDF document loading handler
  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
  };

  // PDF page navigation
  const goToPreviousPage = () => {
    if (pageNumber > 1) {
      setPageNumber(pageNumber - 1);
    }
  };

  const goToNextPage = () => {
    if (numPages && pageNumber < numPages) {
      setPageNumber(pageNumber + 1);
    }
  };

  // Render reader based on book format
  const renderReader = () => {
    if (!book || !bookUrl) return null;

    switch (book.format) {
      case 'epub':
        return <EpubReader url={bookUrl} />;
      
      case 'pdf':
        return (
          <div className="reader-container">
            <Document
              file={bookUrl}
              onLoadSuccess={onDocumentLoadSuccess}
              loading={<div className="text-center py-10">Loading PDF...</div>}
              error={<div className="text-center py-10 text-red-500">Failed to load PDF</div>}
            >
              <Page 
                pageNumber={pageNumber} 
                width={Math.min(800, window.innerWidth - 40)}
                renderTextLayer={false}
                renderAnnotationLayer={false}
              />
            </Document>
            
            <div className="reader-controls">
              <button
                onClick={goToPreviousPage}
                disabled={pageNumber <= 1}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
              >
                <FiArrowLeft className="inline mr-1" /> Previous
              </button>
              <p className="text-sm text-center">
                Page {pageNumber} of {numPages}
              </p>
              <button
                onClick={goToNextPage}
                disabled={!numPages || pageNumber >= numPages}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
              >
                Next <FiArrowRight className="inline ml-1" />
              </button>
            </div>
          </div>
        );
      
      case 'txt':
        // For TXT files, we'd fetch and display the text content
        // This is a simplified implementation
        return (
          <div className="reader-container">
            <div 
              className="reader-content" 
              style={{ fontSize: `${fontSize}px` }}
            >
              {textContent ? (
                <pre className="whitespace-pre-wrap font-serif">{textContent}</pre>
              ) : (
                <div className="text-center py-10">Loading text content...</div>
              )}
            </div>
          </div>
        );
      
      default:
        return <div className="text-center py-10">Unsupported format</div>;
    }
  };

  // Render settings panel
  const renderSettings = () => {
    if (!showSettings) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-10">
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Reader Settings</h3>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Font Size: {fontSize}px
            </label>
            <input
              type="range"
              min="12"
              max="24"
              value={fontSize}
              onChange={(e) => setFontSize(parseInt(e.target.value))}
              className="w-full"
            />
          </div>
          
          <div className="flex justify-end">
            <button
              onClick={() => setShowSettings(false)}
              className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <Layout requireAuth>
        <div className="flex justify-center py-20">
          <div className="w-12 h-12 border-t-4 border-primary-500 border-solid rounded-full animate-spin"></div>
        </div>
      </Layout>
    );
  }

  if (!book) {
    return (
      <Layout requireAuth>
        <div className="text-center py-20">
          <h2 className="text-xl font-medium text-gray-900 dark:text-white mb-4">Book not found</h2>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title={`Reading: ${book.title} - Illuminai`} requireAuth>
      {renderSettings()}
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center mb-4">
          <button
            onClick={() => router.push('/library')}
            className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            <FiArrowLeft className="mr-2 -ml-1 h-5 w-5" />
            Back to Library
          </button>
          
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            <FiSettings className="mr-2 -ml-1 h-5 w-5" />
            Settings
          </button>
        </div>
        
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{book.title}</h1>
          {book.author && (
            <p className="text-gray-600 dark:text-gray-400">by {book.author}</p>
          )}
        </div>
        
        {renderReader()}
      </div>
    </Layout>
  );
};

export default ReadPage;