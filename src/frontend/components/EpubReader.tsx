import React, { useState, useEffect, useRef } from 'react';
import { ReactReader } from 'react-reader';

interface EpubReaderProps {
  url: string;
  bookId: number;
  fontSize?: number;
}

// Use react-reader which is more compatible
const EpubReader: React.FC<EpubReaderProps> = ({ url, bookId, fontSize = 16 }) => {
  const [location, setLocation] = useState<string | number>(0);
  const renditionRef = useRef<any>(null);
  const locationKey = `epub-location-${bookId}`;
  const [isLoading, setIsLoading] = useState(true);

  // Get the saved location from localStorage
  useEffect(() => {
    const savedLocation = localStorage.getItem(locationKey);
    if (savedLocation) {
      setLocation(savedLocation);
    }
  }, [locationKey]);

  // Function to handle location changes
  const locationChanged = (epubcifi: string) => {
    // Save the current location in localStorage
    localStorage.setItem(locationKey, epubcifi);
    setLocation(epubcifi);
  };

  // Custom path transform function to handle EPUB internal paths
  const transformPath = (path: string) => {
    // Extract book ID from the URL
    const bookIdStr = bookId.toString();
    
    // If it's an external URL, return unchanged
    if (path.startsWith('http')) {
      return path;
    }
    
    // Clean the path (remove leading slash if present)
    const cleanPath = path.startsWith('/') ? path.substring(1) : path;
    
    // Construct the path that goes through our backend endpoint
    return `/api/books/${bookIdStr}/${cleanPath}`;
  };

  // Handle loading state
  const handleReady = () => {
    setIsLoading(false);
    console.log("EPUB reader ready!");
  };
  
  // Add console messages for debugging
  useEffect(() => {
    console.log(`Loading EPUB from URL: ${url} for book ID: ${bookId}`);
  }, [url, bookId]);

  return (
    <div className="relative w-full">
      {isLoading && (
        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-80 z-10">
          <div className="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      )}
      
      <div className="w-full h-[calc(100vh-250px)] bg-white rounded-md shadow-md">
        <ReactReader
          url={`${url}?t=${Date.now()}`} // Add timestamp to prevent caching
          title={`Book ${bookId}`}
          location={location}
          locationChanged={locationChanged}
          getRendition={(rendition) => {
            renditionRef.current = rendition;
            
            // Set font size
            rendition.themes.fontSize(`${fontSize}px`);
            
            // Override the resolver functions to use our backend
            if (rendition.book) {
              // Override resolve
              const originalResolve = rendition.book.resolve;
              rendition.book.resolve = function(...args: any[]) {
                const path = originalResolve.apply(rendition.book, args);
                console.log("Resolving path:", path);
                
                // Only apply the transform if it's a relative path
                if (path && typeof path === 'string' && !path.startsWith('http')) {
                  const transformed = transformPath(path);
                  console.log("Transformed to:", transformed);
                  return transformed;
                }
                
                return path;
              };
              
              // Also override resources.resolve
              if (rendition.book.resources) {
                const originalResourceResolve = rendition.book.resources.resolve;
                rendition.book.resources.resolve = function(path: string) {
                  console.log("Resource resolving path:", path);
                  
                  // Transform the path before calling the original resolve
                  if (path && !path.startsWith('http')) {
                    const transformed = transformPath(path);
                    console.log("Resource transformed to:", transformed);
                    return transformed;
                  }
                  
                  return originalResourceResolve.call(rendition.book.resources, path);
                };
              }
            }
            
            // Notify when the book is ready
            rendition.on('rendered', handleReady);
          }}
          epubOptions={{
            flow: 'paginated',
            allowScriptedContent: false,
            allowPopups: false,
          }}
          styles={{
            container: {
              position: 'relative',
              width: '100%',
              height: '100%',
            },
            readerArea: {
              position: 'relative',
              width: '100%',
              height: '100%',
              backgroundColor: 'white',
            },
          }}
          tocChanged={(toc) => {
            console.log('Table of contents loaded:', toc);
          }}
          swipeable
        />
      </div>
      
      <div className="mt-4 flex justify-between">
        <button
          onClick={() => renditionRef.current?.prev()}
          className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded flex items-center"
        >
          <span className="mr-2">←</span> Previous
        </button>
        
        <button
          onClick={() => renditionRef.current?.next()}
          className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded flex items-center"
        >
          Next <span className="ml-2">→</span>
        </button>
      </div>
    </div>
  );
};

export default EpubReader;