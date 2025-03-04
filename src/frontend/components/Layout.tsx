import React, { ReactNode } from 'react';
import Head from 'next/head';
import Navbar from './Navbar';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/router';

interface LayoutProps {
  children: ReactNode;
  title?: string;
  description?: string;
  requireAuth?: boolean;
}

const Layout: React.FC<LayoutProps> = ({
  children,
  title = 'Illuminai - Your Digital Library',
  description = 'Read and manage your e-books with Illuminai',
  requireAuth = false,
}) => {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  // Check if user is authenticated for protected routes
  React.useEffect(() => {
    if (requireAuth && !loading && !isAuthenticated) {
      router.push('/login?redirect=' + router.pathname);
    }
  }, [requireAuth, isAuthenticated, loading, router]);

  // Show loading state while checking authentication
  if (loading && requireAuth) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="w-16 h-16 border-t-4 border-primary-500 border-solid rounded-full animate-spin"></div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="flex flex-col min-h-screen">
        <Navbar />
        <main className="flex-grow">{children}</main>
        <footer className="bg-gray-100 dark:bg-gray-800 py-4 text-center">
          <p>© {new Date().getFullYear()} Illuminai - Open Source E-Book Reader</p>
        </footer>
      </div>
    </>
  );
};

export default Layout;