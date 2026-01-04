import React from 'react';
import ChatWidget from '../components/ChatWidget/ChatWidget';

// This component wraps the entire app and is the perfect place to add global components
export default function Root({children}) {
  return (
    <>
      {children}
      <ChatWidget />
    </>
  );
}
