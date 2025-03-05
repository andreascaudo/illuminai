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
  const [showKeyboardShortcuts, setShowKeyboardShortcuts] = useState<boolean>(false);
  const [theme, setTheme] = useState<string>("light");
  const [lineSpacing, setLineSpacing] = useState<number>(1.5);

  // Fetch book data
  // Load user preferences from localStorage
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const savedFontSize = localStorage.getItem('reader-font-size');
      const savedTheme = localStorage.getItem('reader-theme');
      const savedLineSpacing = localStorage.getItem('reader-line-spacing');
      
      if (savedFontSize) setFontSize(parseInt(savedFontSize));
      if (savedTheme) setTheme(savedTheme);
      if (savedLineSpacing) setLineSpacing(parseFloat(savedLineSpacing));
    }
  }, []);
  
  // Save preferences when they change
  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('reader-font-size', fontSize.toString());
      localStorage.setItem('reader-theme', theme);
      localStorage.setItem('reader-line-spacing', lineSpacing.toString());
    }
  }, [fontSize, theme, lineSpacing]);

  useEffect(() => {
    const fetchBook = async () => {
      if (!id) return;
      
      try {
        // Fetch book details
        const response = await axios.get(`/api/books/${id}`);
        setBook(response.data);
        
        // Get book content URL
        setBookUrl(`/api/books/${id}/content`);
        
        // For TXT files, fetch the content separately
        if (response.data.format === 'txt') {
          const contentResponse = await axios.get(`/api/books/${id}/content`);
          if (contentResponse.data && contentResponse.data.content) {
            setTextContent(contentResponse.data.content);
          }
        }
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
  
  // Add keyboard shortcuts for navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!book) return;
      
      // Skip if inside an input field
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }
      
      switch (e.key) {
        case 'ArrowLeft':
          if (book.format === 'pdf') goToPreviousPage();
          break;
        case 'ArrowRight':
          if (book.format === 'pdf') goToNextPage();
          break;
        case 'Home':
          if (book.format === 'pdf') setPageNumber(1);
          break;
        case 'End':
          if (book.format === 'pdf' && numPages) setPageNumber(numPages);
          break;
        case 's':
          if (e.ctrlKey || e.metaKey) {
            e.preventDefault();
            setShowSettings(!showSettings);
          }
          break;
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [book, pageNumber, numPages, showSettings, goToPreviousPage, goToNextPage]);

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
        return <EpubReader url={bookUrl} fontSize={fontSize} />;
      
      case 'pdf':
        return (
          <div 
            className="reader-container"
            style={{
              backgroundColor: theme === 'light' ? '#f8f9fa' : '#1e293b',
              padding: '2rem',
              borderRadius: '8px',
            }}
          >
            <Document
              file={bookUrl}
              onLoadSuccess={onDocumentLoadSuccess}
              loading={<div className="text-center py-10">Loading PDF...</div>}
              error={<div className="text-center py-10 text-red-500">Failed to load PDF</div>}
              className={theme === 'dark' ? 'invert' : ''}
            >
              <Page 
                pageNumber={pageNumber} 
                width={Math.min(800, window.innerWidth - 40)}
                renderTextLayer={true}
                renderAnnotationLayer={true}
                scale={fontSize / 16} // Scale based on font size setting
              />
            </Document>
            
            <div className="reader-controls mt-4 flex items-center justify-between">
              <div>
                <button
                  onClick={() => setPageNumber(1)}
                  disabled={pageNumber <= 1}
                  className="mr-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
                >
                  First
                </button>
                <button
                  onClick={goToPreviousPage}
                  disabled={pageNumber <= 1}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
                >
                  <FiArrowLeft className="inline mr-1" /> Previous
                </button>
              </div>
              
              <div className="flex items-center">
                <span className="text-sm mr-2">Page</span>
                <input 
                  type="number" 
                  min={1} 
                  max={numPages || 1}
                  value={pageNumber}
                  onChange={(e) => {
                    const value = parseInt(e.target.value);
                    if (value >= 1 && numPages && value <= numPages) {
                      setPageNumber(value);
                    }
                  }}
                  className="w-16 px-2 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm dark:bg-gray-700 dark:text-white"
                />
                <span className="text-sm mx-2">of {numPages}</span>
              </div>
              
              <div>
                <button
                  onClick={goToNextPage}
                  disabled={!numPages || pageNumber >= numPages}
                  className="mr-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
                >
                  Next <FiArrowRight className="inline ml-1" />
                </button>
                <button
                  onClick={() => numPages && setPageNumber(numPages)}
                  disabled={!numPages || pageNumber >= numPages}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50"
                >
                  Last
                </button>
              </div>
            </div>
          </div>
        );
      
      case 'txt':
        return (
          <div className="reader-container">
            <div 
              className="reader-content" 
              style={{ 
                fontSize: `${fontSize}px`,
                lineHeight: lineSpacing,
                backgroundColor: theme === 'light' ? '#f8f9fa' : '#1e293b',
                color: theme === 'light' ? '#333' : '#e2e8f0',
                padding: '2rem',
                borderRadius: '8px',
              }}
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
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Line Spacing: {lineSpacing}
            </label>
            <input
              type="range"
              min="1"
              max="3"
              step="0.1"
              value={lineSpacing}
              onChange={(e) => setLineSpacing(parseFloat(e.target.value))}
              className="w-full"
            />
          </div>
          
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Theme
            </label>
            <div className="flex space-x-4">
              <button
                onClick={() => setTheme('light')}
                className={`px-3 py-2 rounded-md ${
                  theme === 'light' 
                    ? 'bg-primary-100 text-primary-800 border-2 border-primary-500' 
                    : 'bg-gray-100 text-gray-800 border-2 border-transparent'
                }`}
              >
                Light
              </button>
              <button
                onClick={() => setTheme('dark')}
                className={`px-3 py-2 rounded-md ${
                  theme === 'dark' 
                    ? 'bg-gray-700 text-gray-100 border-2 border-primary-500' 
                    : 'bg-gray-700 text-gray-100 border-2 border-transparent'
                }`}
              >
                Dark
              </button>
            </div>
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

  // Render keyboard shortcuts helper
  const renderKeyboardShortcuts = () => {
    if (!showKeyboardShortcuts) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-10">
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Keyboard Shortcuts</h3>
          
          <div className="space-y-3 mb-6">
            <div className="flex justify-between">
              <span className="text-gray-700 dark:text-gray-300">Open Settings</span>
              <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">Ctrl/⌘ + S</code>
            </div>
            
            {book?.format === 'pdf' && (
              <>
                <div className="flex justify-between">
                  <span className="text-gray-700 dark:text-gray-300">Previous Page</span>
                  <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">←</code>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700 dark:text-gray-300">Next Page</span>
                  <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">→</code>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700 dark:text-gray-300">First Page</span>
                  <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">Home</code>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700 dark:text-gray-300">Last Page</span>
                  <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">End</code>
                </div>
              </>
            )}
            
            {book?.format === 'epub' && (
              <>
                <div className="flex justify-between">
                  <span className="text-gray-700 dark:text-gray-300">Previous Page</span>
                  <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">←</code>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-700 dark:text-gray-300">Next Page</span>
                  <code className="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">→</code>
                </div>
              </>
            )}
          </div>
          
          <div className="flex justify-end">
            <button
              onClick={() => setShowKeyboardShortcuts(false)}
              className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    );
  };

  return (
    <Layout title={`Reading: ${book.title} - Illuminai`} requireAuth>
      {renderSettings()}
      {renderKeyboardShortcuts()}
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-between items-center mb-4">
          <button
            onClick={() => router.push('/library')}
            className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            <FiArrowLeft className="mr-2 -ml-1 h-5 w-5" />
            Back to Library
          </button>
          
          <div className="flex space-x-2">
            <button
              onClick={() => setShowKeyboardShortcuts(true)}
              className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <span className="mr-2">⌨️</span>
              Shortcuts
            </button>
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              <FiSettings className="mr-2 -ml-1 h-5 w-5" />
              Settings
            </button>
          </div>
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