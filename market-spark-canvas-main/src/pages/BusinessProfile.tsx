import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Building2, Users, TrendingUp, Target, ArrowRight, Sparkles } from "lucide-react";

const BusinessProfile = () => {
  const features = [
    {
      icon: Building2,
      title: "Profil Business",
      description: "Creează și gestionează profilul afacerii tale cu putere și precizie",
      status: "Activ"
    },
    {
      icon: Users,
      title: "Audiența Țintă",
      description: "Identifică și domină piața cu strategii de targetare avansate",
      status: "În dezvoltare"
    },
    {
      icon: TrendingUp,
      title: "Analiză Performanță",
      description: "Monitorizează și amplifică succesul cu metrici robuste",
      status: "Nou"
    },
    {
      icon: Target,
      title: "Obiective Smart",
      description: "Stabilește și cucerește obiective măsurabile și ambițioase",
      status: "Recomandat"
    }
  ];

  return (
    <div className="min-h-screen bg-black">
      {/* Hero Section - Robust */}
      <section className="relative px-6 py-24 bg-gradient-to-br from-black via-gray-900 to-black">
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center space-x-3 bg-black border-2 border-yellow-400 px-6 py-3 rounded-full mb-8 shadow-lg shadow-yellow-400/20">
            <Sparkles size={20} className="text-yellow-400" />
            <span className="text-sm font-black text-yellow-400 uppercase tracking-wider">
              AI-Powered Business Domination
            </span>
          </div>
          
          <h1 className="text-6xl md:text-7xl font-black text-yellow-400 mb-8 leading-tight tracking-tight">
            Dominează piața cu
            <span className="block text-yellow-400 animate-pulse-robust">inteligența artificială</span>
          </h1>
          
          <p className="text-xl text-yellow-400/80 mb-12 max-w-3xl mx-auto leading-relaxed font-bold">
            Transformă-ți viziunea în imperiu digital. 
            Tinkerbell îți oferă arsenalul complet pentru a cuceri piața și a-ți amplifica impactul.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-6 justify-center">
            <Button size="lg" className="robust-button px-12 py-6 text-lg font-black uppercase tracking-wider">
              Începe Dominația
              <ArrowRight size={24} className="ml-3" />
            </Button>
            <Button variant="outline" size="lg" className="border-2 border-yellow-400 text-yellow-400 hover:bg-yellow-400 hover:text-black px-12 py-6 text-lg font-black uppercase tracking-wider bg-black">
              Descoperă Puterea
            </Button>
          </div>
        </div>
      </section>

      {/* Features Grid - Robust */}
      <section className="px-6 py-20 bg-black">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-4xl font-black text-yellow-400 mb-6 uppercase tracking-wider">
              Arsenal Complet pentru Succes
            </h2>
            <p className="text-xl text-yellow-400/70 max-w-3xl mx-auto font-bold">
              Instrumente de putere pentru liderii de mâine
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card key={index} className="robust-card group p-8">
                  <CardHeader className="pb-6">
                    <div className="flex items-center justify-between mb-6">
                      <div className="p-4 rounded-xl bg-black border-2 border-yellow-400 group-hover:bg-yellow-400 group-hover:border-yellow-500 transition-all duration-300 shadow-lg shadow-yellow-400/20">
                        <Icon size={32} className="text-yellow-400 group-hover:text-black transition-colors duration-300" />
                      </div>
                      <Badge variant="secondary" className="bg-yellow-400/10 text-yellow-400 border-2 border-yellow-400/30 font-bold uppercase tracking-wider px-4 py-2">
                        {feature.status}
                      </Badge>
                    </div>
                    <CardTitle className="text-2xl text-yellow-400 group-hover:text-yellow-300 transition-colors font-black uppercase">
                      {feature.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-yellow-400/70 leading-relaxed text-lg font-bold">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section - Robust */}
      <section className="px-6 py-24 bg-gradient-to-br from-black via-gray-900 to-black">
        <div className="max-w-5xl mx-auto">
          <Card className="robust-card p-20 text-center shadow-2xl shadow-yellow-400/30 border-4 border-yellow-400/40">
            <CardContent className="space-y-10">
              <h3 className="text-5xl font-black text-yellow-400 mb-8 uppercase tracking-widest drop-shadow-lg">
                Ești pregătit să-ți cucerești piața?
              </h3>
              <p className="text-2xl text-yellow-300/90 mb-10 max-w-3xl mx-auto font-extrabold leading-relaxed">
                Fă parte din elita antreprenorilor care transformă ideile în imperii digitale. Acum e momentul să acționezi!
              </p>
              <Button
                size="lg"
                className="robust-button px-20 py-8 text-2xl font-black uppercase tracking-wider animate-pulse-robust bg-yellow-400 text-black hover:bg-yellow-300 transition-all duration-300 shadow-lg shadow-yellow-400/30"
              >
                Creează-ți Imperiul Acum
                <ArrowRight size={32} className="ml-5" />
              </Button>
              <div className="mt-6">
                <span className="text-yellow-400/70 text-lg font-bold">
                  Nu rata șansa de a domina cu inteligență artificială!
                </span>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  );
};

export default BusinessProfile;
