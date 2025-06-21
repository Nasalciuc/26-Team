
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Facebook, Users, Calendar, Star, Plus } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const MarketExploration = () => {
  const [addedToPlan, setAddedToPlan] = useState<string[]>([]);
  const { toast } = useToast();

  const facebookGroups = [
    {
      id: "fb1",
      title: "Antreprenori Moldova 🇲🇩",
      description: "Comunitatea antreprenorilor din Moldova. 15.3K membri activi.",
      relevanceScore: 5,
      members: "15.3K",
      category: "Antreprenoriat"
    },
    {
      id: "fb2", 
      title: "Business Networking Chișinău",
      description: "Networking pentru profesioniști și antreprenori din capitală.",
      relevanceScore: 4,
      members: "8.7K",
      category: "Networking"
    },
    {
      id: "fb3",
      title: "Startup Moldova Community",
      description: "Comunitate pentru startup-uri și idei inovatoare din Moldova.",
      relevanceScore: 4,
      members: "12.1K", 
      category: "Startup"
    }
  ];

  const influencers = [
    {
      id: "inf1",
      title: "Ana Ciobanu",
      description: "Business coach cu 25K followeri. Focus pe antreprenoriat feminin.",
      relevanceScore: 5,
      followers: "25K",
      engagement: "4.2%"
    },
    {
      id: "inf2",
      title: "Mihai Popescu", 
      description: "Marketing specialist cu experiență în creșterea afacerilor locale.",
      relevanceScore: 4,
      followers: "18K",
      engagement: "3.8%"
    },
    {
      id: "inf3",
      title: "Elena Rusu",
      description: "Consultant în dezvoltarea brandurilor mici și mijlocii.",
      relevanceScore: 4,
      followers: "22K",
      engagement: "4.1%"
    }
  ];

  const events = [
    {
      id: "ev1",
      title: "Business Forum Chișinău 2024",
      description: "Eveniment anual pentru antreprenori și investitori. 500+ participanți.",
      relevanceScore: 5,
      date: "15 Mar 2024",
      attendees: "500+"
    },
    {
      id: "ev2",
      title: "Startup Weekend Moldova",
      description: "Weekend intensiv pentru dezvoltarea ideilor de business inovatoare.",
      relevanceScore: 4,
      date: "22-24 Mar 2024", 
      attendees: "150+"
    },
    {
      id: "ev3",
      title: "Digital Marketing Summit",
      description: "Conferință despre ultimele tendințe în marketing digital.",
      relevanceScore: 4,
      date: "5 Apr 2024",
      attendees: "300+"
    }
  ];

  const handleAddToPlan = (id: string, type: string, title: string) => {
    setAddedToPlan([...addedToPlan, id]);
    toast({
      title: "Adăugat în plan!",
      description: `${title} a fost adăugat în planul tău de marketing.`,
    });
  };

  const renderStars = (score: number) => {
    return (
      <div className="flex items-center space-x-1">
        {[...Array(5)].map((_, i) => (
          <Star 
            key={i} 
            className={`w-4 h-4 ${i < score ? "text-yellow-400 fill-current" : "text-gray-600"}`}
          />
        ))}
        <span className="text-sm text-muted-foreground ml-1">({score}/5)</span>
      </div>
    );
  };

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8 animate-fade-in">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold text-gradient">
          Explorează Piața
        </h1>
        <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
          Am identificat cele mai relevante oportunități pentru afacerea ta. 
          Adaugă-le în planul de marketing pentru a începe să te conectezi cu clienții ideali.
        </p>
      </div>

      {/* Facebook Groups */}
      <div className="space-y-6">
        <div className="flex items-center space-x-3">
          <Facebook className="w-6 h-6 text-blue-500" />
          <h2 className="text-2xl font-semibold">Grupuri Facebook Recomandate</h2>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {facebookGroups.map((group) => (
            <Card key={group.id} className="card-hover">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle className="text-lg">{group.title}</CardTitle>
                  <Badge variant="secondary">{group.category}</Badge>
                </div>
                <CardDescription>{group.description}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Membri:</span>
                  <span className="font-semibold">{group.members}</span>
                </div>
                
                <div className="space-y-2">
                  <span className="text-sm text-muted-foreground">Scor de Relevanță:</span>
                  {renderStars(group.relevanceScore)}
                </div>
                
                <Button 
                  onClick={() => handleAddToPlan(group.id, "group", group.title)}
                  disabled={addedToPlan.includes(group.id)}
                  className="w-full"
                  variant={addedToPlan.includes(group.id) ? "secondary" : "default"}
                >
                  {addedToPlan.includes(group.id) ? (
                    "✅ Adăugat în plan"
                  ) : (
                    <>
                      <Plus className="w-4 h-4 mr-2" />
                      Adaugă în plan
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Influencers */}
      <div className="space-y-6">
        <div className="flex items-center space-x-3">
          <Users className="w-6 h-6 text-purple-500" />
          <h2 className="text-2xl font-semibold">Influenceri Locali Recomandați</h2>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {influencers.map((influencer) => (
            <Card key={influencer.id} className="card-hover">
              <CardHeader>
                <CardTitle className="text-lg">{influencer.title}</CardTitle>
                <CardDescription>{influencer.description}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-muted-foreground">Followeri:</span>
                    <div className="font-semibold">{influencer.followers}</div>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Engagement:</span>
                    <div className="font-semibold text-green-400">{influencer.engagement}</div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <span className="text-sm text-muted-foreground">Scor de Relevanță:</span>
                  {renderStars(influencer.relevanceScore)}
                </div>
                
                <Button 
                  onClick={() => handleAddToPlan(influencer.id, "influencer", influencer.title)}
                  disabled={addedToPlan.includes(influencer.id)}
                  className="w-full"
                  variant={addedToPlan.includes(influencer.id) ? "secondary" : "default"}
                >
                  {addedToPlan.includes(influencer.id) ? (
                    "✅ Adăugat în plan"
                  ) : (
                    <>
                      <Plus className="w-4 h-4 mr-2" />
                      Adaugă în plan
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Events */}
      <div className="space-y-6">
        <div className="flex items-center space-x-3">
          <Calendar className="w-6 h-6 text-cyan-500" />
          <h2 className="text-2xl font-semibold">Evenimente Locale Relevante</h2>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {events.map((event) => (
            <Card key={event.id} className="card-hover">
              <CardHeader>
                <CardTitle className="text-lg">{event.title}</CardTitle>
                <CardDescription>{event.description}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-muted-foreground">Data:</span>
                    <div className="font-semibold">{event.date}</div>
                  </div>
                  <div>
                    <span className="text-muted-foreground">Participanți:</span>
                    <div className="font-semibold text-blue-400">{event.attendees}</div>
                  </div>
                </div>
                
                <div className="space-y-2">
                  <span className="text-sm text-muted-foreground">Scor de Relevanță:</span>
                  {renderStars(event.relevanceScore)}
                </div>
                
                <Button 
                  onClick={() => handleAddToPlan(event.id, "event", event.title)}
                  disabled={addedToPlan.includes(event.id)}
                  className="w-full"
                  variant={addedToPlan.includes(event.id) ? "secondary" : "default"}
                >
                  {addedToPlan.includes(event.id) ? (
                    "✅ Adăugat în plan"
                  ) : (
                    <>
                      <Plus className="w-4 h-4 mr-2" />
                      Adaugă în plan
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {addedToPlan.length > 0 && (
        <div className="text-center pt-8">
          <Button 
            size="lg" 
            className="gradient-bg hover:opacity-90"
            onClick={() => window.location.href = '/campanii'}
          >
            Continuă cu Campaniile ({addedToPlan.length} adăugate)
          </Button>
        </div>
      )}
    </div>
  );
};

export default MarketExploration;
