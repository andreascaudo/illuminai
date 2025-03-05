import React, { useState, useEffect, useRef } from 'react';
import { ReactReader } from 'react-reader';

interface EpubReaderProps {
  url: string;
  fontSize?: number;
}

const EpubReader: React.FC<EpubReaderProps> = ({ url, fontSize = 16 }) => {
  const [location, setLocation] = useState<string | number>(0);
  const [size, setSize] = useState<{ width: number; height: number }>({
    width: 600,
    height: 800,
  });
  const renditionRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Store reader location in localStorage
  const locationChanged = (epubcifi: string) => {
    // epubcifi is a string that describes the position in the book
    setLocation(epubcifi);
    
    // Save the location to localStorage
    if (typeof window !== 'undefined' && url) {
      localStorage.setItem(`book-location-${url}`, epubcifi);
    }
  };

  // Get the saved location from localStorage
  useEffect(() => {
    if (typeof window !== 'undefined' && url) {
      const savedLocation = localStorage.getItem(`book-location-${url}`);
      if (savedLocation) {
        setLocation(savedLocation);
      }
    }
  }, [url]);

  // Update reader size based on container
  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        const { offsetWidth, offsetHeight } = containerRef.current;
        setSize({
          width: offsetWidth,
          height: offsetHeight,
        });
      }
    };

    // Initial size
    updateSize();

    // Update on resize
    window.addEventListener('resize', updateSize);
    return () => window.removeEventListener('resize', updateSize);
  }, []);

  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!renditionRef.current) return;
      
      if (e.key === 'ArrowLeft') {
        renditionRef.current.prev();
      } else if (e.key === 'ArrowRight') {
        renditionRef.current.next();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);
  
  // Update font size when it changes
  useEffect(() => {
    if (renditionRef.current) {
      renditionRef.current.themes.fontSize(`${fontSize}px`);
    }
  }, [fontSize]);

  return (
    <div 
      ref={containerRef} 
      className="reader-container" 
      style={{ height: 'calc(100vh - 200px)', width: '100%' }}
    >
      <ReactReader
        url={url}
        location={location}
        locationChanged={locationChanged}
        getRendition={(rendition) => {
          renditionRef.current = rendition;
          
          // Set font size
          rendition.themes.fontSize(`${fontSize}px`);
          
          // Add swipe events for page turning
          rendition.on('touchstart', (e: any) => {
            const touchStartX = e.changedTouches[0].screenX;
            
            rendition.on('touchend', (e: any) => {
              const touchEndX = e.changedTouches[0].screenX;
              const diff = touchStartX - touchEndX;
              
              if (diff > 50) {
                rendition.next();
              } else if (diff < -50) {
                rendition.prev();
              }
            });
          });
        }}
        epubOptions={{
          flow: 'paginated',
          width: size.width,
          height: size.height,
        }}
        swipeable
      />
    </div>
  );
};

export default EpubReader;