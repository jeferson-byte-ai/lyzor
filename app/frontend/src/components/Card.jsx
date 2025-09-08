import React from 'react';
export default function Card({ title, value }) {
  return (
    <div className="bg-zinc-800 rounded-lg p-6 shadow-md w-64">
      <div className="text-xl font-bold mb-2">{title}</div>
      <div className="text-3xl font-extrabold text-lyzor">{value}</div>
    </div>
  );
}