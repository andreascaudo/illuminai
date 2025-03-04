import Layout from '@/components/Layout';
import Link from 'next/link';
import { FiBook, FiUpload, FiSmartphone, FiCloud, FiShield } from 'react-icons/fi';

export default function Home() {
  return (
    <Layout>
      <div className="bg-gradient-to-b from-white to-gray-100 dark:from-gray-900 dark:to-gray-800">
        {/* Hero Section */}
        <section className="py-20 px-4 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">Your Books, Anywhere</h1>
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
            Upload, organize, and read your e-books with a beautiful, distraction-free experience.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/register"
              className="px-8 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 font-medium text-lg"
            >
              Get Started
            </Link>
            <Link
              href="/login"
              className="px-8 py-3 bg-white dark:bg-gray-800 text-primary-600 dark:text-primary-400 border border-primary-600 dark:border-primary-400 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 font-medium text-lg"
            >
              Log In
            </Link>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-16 px-4 max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Features</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
              <FiBook className="text-primary-500 text-4xl mb-4" />
              <h3 className="text-xl font-semibold mb-2">E-book Reader</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Read your e-books in a clean, customizable interface with features like bookmarks, highlights, and adjustable text.
              </p>
            </div>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
              <FiUpload className="text-primary-500 text-4xl mb-4" />
              <h3 className="text-xl font-semibold mb-2">Upload & Organize</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Easily upload your .epub, .pdf, and .txt files. Organize your books with tags and collections.
              </p>
            </div>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
              <FiSmartphone className="text-primary-500 text-4xl mb-4" />
              <h3 className="text-xl font-semibold mb-2">Cross-Platform</h3>
              <p className="text-gray-600 dark:text-gray-300">
                Access your books from any device. Mobile apps coming soon for iOS and Android.
              </p>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="py-16 px-4 bg-gray-50 dark:bg-gray-800">
          <div className="max-w-7xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="bg-primary-100 dark:bg-primary-900 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">1</span>
                </div>
                <h3 className="text-xl font-semibold mb-2">Create an Account</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Sign up for free and get access to your personal library.
                </p>
              </div>
              <div className="text-center">
                <div className="bg-primary-100 dark:bg-primary-900 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">2</span>
                </div>
                <h3 className="text-xl font-semibold mb-2">Upload Your Books</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Upload your e-books in EPUB, PDF, or TXT formats.
                </p>
              </div>
              <div className="text-center">
                <div className="bg-primary-100 dark:bg-primary-900 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">3</span>
                </div>
                <h3 className="text-xl font-semibold mb-2">Start Reading</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Enjoy your books with our beautiful reader interface.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Open Source Section */}
        <section className="py-16 px-4 max-w-7xl mx-auto">
          <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md">
            <h2 className="text-3xl font-bold mb-4">Open Source Project</h2>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              Illuminai is an open-source project, free to use and modify. Contributions are welcome!
            </p>
            <a
              href="https://github.com/yourusername/illuminai"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center text-primary-600 dark:text-primary-400 hover:underline"
            >
              View on GitHub
              <svg className="ml-1 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd"></path>
              </svg>
            </a>
          </div>
        </section>
      </div>
    </Layout>
  );
}