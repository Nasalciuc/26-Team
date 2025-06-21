
import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Home } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error(
      "404 Error: User attempted to access non-existent route:",
      location.pathname
    );
  }, [location.pathname]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center space-y-6 max-w-md mx-auto p-6">
        <div className="text-8xl font-bold text-gradient">
          404
        </div>
        <div className="space-y-2">
          <h1 className="text-2xl font-bold">Pagină Inexistentă</h1>
          <p className="text-muted-foreground">
            Ne pare rău, pagina pe care o cauți nu poate fi găsită.
          </p>
        </div>
        <Link to="/">
          <Button className="gradient-bg hover:opacity-90">
            <Home className="w-4 h-4 mr-2" />
            Înapoi Acasă
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default NotFound;
