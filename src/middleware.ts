import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const authCookie = request.cookies.get('auth');
  
  // Allow access if already authenticated
  if (authCookie?.value === 'authenticated') {
    return NextResponse.next();
  }
  
  // Allow the login page and API
  if (request.nextUrl.pathname === '/login' || request.nextUrl.pathname === '/api/auth') {
    return NextResponse.next();
  }
  
  // Redirect to login
  return NextResponse.redirect(new URL('/login', request.url));
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
