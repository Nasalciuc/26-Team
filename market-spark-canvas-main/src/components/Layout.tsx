
import { Link, useLocation } from "react-router-dom";
import { User, Search, Megaphone, Menu, X } from "lucide-react";
import { useState } from "react";

const Layout = ({ children }: { children: React.ReactNode }) => {
  const location = useLocation();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigation = [
    { name: "Despre mine", href: "/", icon: User },
    { name: "Explorează Piața", href: "/explorare", icon: Search },
    { name: "Campanii", href: "/campanii", icon: Megaphone },
  ];

  return (
    <div className="min-h-screen bg-black">
      {/* Robust Black Header */}
      <header className="sticky top-0 z-50 bg-black/95 backdrop-blur-md border-b-2 border-gray-800">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex items-center justify-between h-20">
            {/* Logo Section - Robust Design */}
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-yellow-400 to-yellow-600 flex items-center justify-center shadow-xl border-2 border-yellow-400/50">
                <span className="text-black font-black text-xl">T</span>
              </div>
              <div>
                <h1 className="text-3xl font-black text-yellow-400 tracking-tight">
                  Tinkerbell
                </h1>
                <p className="text-xs text-yellow-400/70 font-bold uppercase tracking-wider">
                  AI pentru afaceri mici
                </p>
              </div>
            </div>
            
            {/* Desktop Navigation - Robust Style */}
            <nav className="hidden md:flex items-center space-x-2">
              {navigation.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href;
                
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center space-x-3 px-6 py-4 rounded-lg transition-all duration-300 border-2 font-bold ${
                      isActive
                        ? "bg-yellow-400 text-black border-yellow-400 shadow-lg shadow-yellow-400/50"
                        : "text-yellow-400 border-gray-800 hover:bg-gray-900 hover:border-yellow-400/50 hover:shadow-lg hover:shadow-yellow-400/20"
                    }`}
                  >
                    <Icon size={22} className={isActive ? "text-black" : "text-yellow-400"} />
                    <span className="font-bold text-sm uppercase tracking-wide">{item.name}</span>
                  </Link>
                );
              })}
            </nav>

            {/* Mobile Menu Button - Robust */}
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="md:hidden p-3 rounded-lg border-2 border-yellow-400 text-yellow-400 hover:bg-yellow-400 hover:text-black transition-all duration-300"
            >
              {isMobileMenuOpen ? (
                <X size={24} />
              ) : (
                <Menu size={24} />
              )}
            </button>
          </div>

          {/* Mobile Navigation - Robust */}
          {isMobileMenuOpen && (
            <div className="md:hidden pb-6 animate-fade-in">
              <nav className="space-y-3 bg-gray-900/50 p-4 rounded-lg border-2 border-gray-800">
                {navigation.map((item) => {
                  const Icon = item.icon;
                  const isActive = location.pathname === item.href;
                  
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      onClick={() => setIsMobileMenuOpen(false)}
                      className={`flex items-center space-x-4 px-6 py-4 rounded-lg transition-all duration-300 border-2 font-bold ${
                        isActive
                          ? "bg-yellow-400 text-black border-yellow-400"
                          : "text-yellow-400 border-gray-700 hover:bg-gray-800 hover:border-yellow-400/50"
                      }`}
                    >
                      <Icon size={20} />
                      <span className="font-bold uppercase tracking-wide">{item.name}</span>
                    </Link>
                  );
                })}
              </nav>
            </div>
          )}
        </div>
      </header>
      
      {/* Main Content */}
      <main className="relative bg-black min-h-screen">
        {children}
      </main>

      {/* Robust Footer */}
      <footer className="border-t-2 border-gray-800 mt-20 bg-black">
        <div className="max-w-6xl mx-auto px-6 py-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-yellow-400 to-yellow-600 flex items-center justify-center border-2 border-yellow-400/50">
                <span className="text-black font-black text-lg">T</span>
              </div>
              <span className="text-sm text-yellow-400 font-bold">
                © 2024 Tinkerbell - AI pentru afaceri mici
              </span>
            </div>
            <div className="text-xs text-yellow-400/70 font-bold uppercase tracking-wider">
              Creat cu ❤️ pentru succesul tău
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
