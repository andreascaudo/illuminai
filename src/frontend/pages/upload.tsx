import React, { useState, useCallback } from 'react';
import Layout from '@/components/Layout';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { toast } from 'react-toastify';
import { useRouter } from 'next/router';
import { FiUpload, FiFile, FiX } from 'react-icons/fi';

const Upload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    author: '',
    description: '',
  });
  const [uploading, setUploading] = useState(false);
  const router = useRouter();

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const selectedFile = acceptedFiles[0];
      // Check file type
      const validTypes = ['.epub', '.pdf', '.txt'];
      const fileExtension = selectedFile.name.substring(selectedFile.name.lastIndexOf('.')).toLowerCase();
      
      if (!validTypes.includes(fileExtension)) {
        toast.error('Invalid file type. Please upload an EPUB, PDF, or TXT file.');
        return;
      }
      
      setFile(selectedFile);
      
      // Try to extract title from filename
      const fileName = selectedFile.name.substring(0, selectedFile.name.lastIndexOf('.'));
      setFormData((prev) => ({
        ...prev,
        title: fileName,
      }));
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles: 1,
    accept: {
      'application/epub+zip': ['.epub'],
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
    },
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!file) {
      toast.error('Please select a file to upload');
      return;
    }
    
    if (!formData.title.trim()) {
      toast.error('Please enter a title for your book');
      return;
    }
    
    setUploading(true);
    
    // Create form data for file upload
    const uploadData = new FormData();
    uploadData.append('file', file);
    uploadData.append('title', formData.title);
    
    if (formData.author.trim()) {
      uploadData.append('author', formData.author);
    }
    
    if (formData.description.trim()) {
      uploadData.append('description', formData.description);
    }
    
    try {
      await axios.post('/api/books/upload', uploadData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      toast.success('Book uploaded successfully!');
      router.push('/library');
    } catch (error) {
      console.error('Upload error:', error);
      toast.error('Failed to upload book. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const clearFile = () => {
    setFile(null);
  };

  return (
    <Layout title="Upload Book - Illuminai" requireAuth>
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">Upload Book</h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {!file ? (
            <div 
              {...getRootProps()} 
              className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
                isDragActive 
                  ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' 
                  : 'border-gray-300 dark:border-gray-700 hover:border-primary-500 dark:hover:border-primary-500'
              }`}
            >
              <input {...getInputProps()} />
              <FiUpload className="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500" />
              <p className="mt-2 text-sm font-medium text-gray-900 dark:text-white">
                {isDragActive ? 'Drop the file here' : 'Drag and drop a file here, or click to select a file'}
              </p>
              <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                Supported formats: EPUB, PDF, TXT
              </p>
            </div>
          ) : (
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 flex items-center justify-between">
              <div className="flex items-center overflow-hidden">
                <FiFile className="flex-shrink-0 h-6 w-6 text-primary-500" />
                <div className="ml-4 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                    {file.name}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={clearFile}
                className="ml-4 flex-shrink-0 p-1 rounded-full text-gray-400 hover:text-gray-500 dark:text-gray-500 dark:hover:text-gray-400"
              >
                <FiX className="h-5 w-5" />
              </button>
            </div>
          )}
          
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Title*
            </label>
            <div className="mt-1">
              <input
                type="text"
                name="title"
                id="title"
                required
                value={formData.title}
                onChange={handleChange}
                className="block w-full rounded-md border-gray-300 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm dark:bg-gray-800 dark:text-white"
              />
            </div>
          </div>
          
          <div>
            <label htmlFor="author" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Author
            </label>
            <div className="mt-1">
              <input
                type="text"
                name="author"
                id="author"
                value={formData.author}
                onChange={handleChange}
                className="block w-full rounded-md border-gray-300 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm dark:bg-gray-800 dark:text-white"
              />
            </div>
          </div>
          
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Description
            </label>
            <div className="mt-1">
              <textarea
                name="description"
                id="description"
                rows={4}
                value={formData.description}
                onChange={handleChange}
                className="block w-full rounded-md border-gray-300 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm dark:bg-gray-800 dark:text-white"
              />
            </div>
          </div>
          
          <div>
            <button
              type="submit"
              disabled={!file || uploading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {uploading ? 'Uploading...' : 'Upload Book'}
            </button>
          </div>
        </form>
      </div>
    </Layout>
  );
};

export default Upload;