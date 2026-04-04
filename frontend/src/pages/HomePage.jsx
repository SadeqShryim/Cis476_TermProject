/**
 * HomePage — public landing page with hero, features overview, and CTAs.
 */
import { Link } from 'react-router-dom';
import { Car, Search, Shield, MessageSquare, Star, CreditCard } from 'lucide-react';

const features = [
  { icon: Car,            title: 'List Your Car',      desc: 'Owners can list vehicles with full details, pricing, and availability calendars.' },
  { icon: Search,         title: 'Search & Book',      desc: 'Find the perfect ride by location, date, price, and more — then book instantly.' },
  { icon: Shield,         title: 'Secure Payments',    desc: 'Simulated payment system with balance tracking and instant notifications.' },
  { icon: MessageSquare,  title: 'In-App Messaging',   desc: 'Communicate directly with owners or renters through built-in messaging.' },
  { icon: Star,           title: 'Reviews & Ratings',  desc: 'Leave and read reviews to build trust in the community.' },
  { icon: CreditCard,     title: 'Watch & Get Alerts', desc: 'Watch cars and get notified when prices drop to your target.' },
];

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-white">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-8 py-4 bg-white/80 backdrop-blur border-b border-gray-200">
        <Link to="/" className="text-2xl font-bold text-purple-700">DriveShare</Link>
        <div className="flex gap-3">
          <Link to="/login" className="px-4 py-2 text-sm font-medium text-purple-700 border border-purple-300 rounded-lg hover:bg-purple-50">
            Log In
          </Link>
          <Link to="/register" className="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700">
            Sign Up
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="flex flex-col items-center justify-center px-6 py-24 text-center">
        <h1 className="text-5xl font-bold text-gray-900 leading-tight max-w-2xl">
          Peer-to-Peer Car Rentals, <span className="text-purple-600">Made Simple</span>
        </h1>
        <p className="mt-4 text-lg text-gray-600 max-w-xl">
          Rent cars directly from owners in your area, or list your own vehicle and earn money while it sits idle.
        </p>
        <div className="mt-8 flex gap-4">
          <Link to="/register" className="px-6 py-3 text-white bg-purple-600 rounded-lg font-medium hover:bg-purple-700">
            Get Started
          </Link>
          <Link to="/login" className="px-6 py-3 text-purple-700 border border-purple-300 rounded-lg font-medium hover:bg-purple-50">
            Log In
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="px-8 py-16 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Everything You Need</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="p-6 bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
              <div className="w-10 h-10 flex items-center justify-center rounded-lg bg-purple-100 text-purple-600 mb-4">
                <Icon size={20} />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
              <p className="text-sm text-gray-600">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="text-center py-8 text-sm text-gray-500 border-t border-gray-200">
        DriveShare &mdash; CIS 476 Term Project
      </footer>
    </div>
  );
}
