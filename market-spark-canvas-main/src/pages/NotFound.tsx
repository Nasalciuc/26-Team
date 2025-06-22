import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Home, ArrowLeft, Search } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      <div className="text-center space-y-8 max-w-lg mx-auto p-8">
        <div className="relative">
          <div className="text-9xl font-black bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
            404
          </div>
          <div className="absolute -inset-4 bg-gradient-to-r from-blue-500/20 to-purple-500/20 rounded-full blur-xl"></div>
        </div>

        <div className="space-y-4">
          <h1 className="text-3xl font-bold text-gray-800">
            Oops! Pagină Inexistentă
          </h1>
          <p className="text-lg text-gray-600 leading-relaxed">
            Ne pare rău, pagina pe care o cauți nu poate fi găsită. Poate a fost
            mutată sau nu există.
          </p>
          <div className="text-sm text-gray-500 bg-gray-100 rounded-lg p-3 border-l-4 border-blue-500">
            <strong>Ruta accesată:</strong> {location.pathname}
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
          <Link to="/">
            <Button className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-6 py-3 text-lg font-semibold shadow-lg">
              <Home className="w-5 h-5 mr-2" />
              Înapoi Acasă
            </Button>
          </Link>

          <Button
            variant="outline"
            onClick={() => window.history.back()}
            className="border-2 border-gray-300 hover:border-blue-400 px-6 py-3 text-lg font-semibold"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Pagina Anterioară
          </Button>
        </div>

        <div className="pt-8 border-t border-gray-200">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">
            Poate te interesează:
          </h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
            <Link
              to="/business-profile"
              className="p-3 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all text-gray-700 hover:text-blue-600"
            >
              📊 Profil Business
            </Link>
            <Link
              to="/campaigns"
              className="p-3 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all text-gray-700 hover:text-blue-600"
            >
              🚀 Campanii Marketing
            </Link>
            <Link
              to="/market-exploration"
              className="p-3 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all text-gray-700 hover:text-blue-600"
            >
              🔍 Explorare Piață
            </Link>
            <Link
              to="/analytics"
              className="p-3 bg-white rounded-lg border border-gray-200 hover:border-blue-300 hover:shadow-md transition-all text-gray-700 hover:text-blue-600"
            >
              📈 Analiză Performanță
            </Link>
          </div>
        </div>

        <div className="text-xs text-gray-400 pt-4">
          Dacă problema persistă, te rugăm să ne contactezi pentru asistență.
        </div>
      </div>
    </div>
  );
};

export default NotFound;
