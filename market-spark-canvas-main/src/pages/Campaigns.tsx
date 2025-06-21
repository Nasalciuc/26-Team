
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Sparkles, Image, MessageSquare, Calendar, Edit, Check } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const Campaigns = () => {
  const [campaignTitle, setCampaignTitle] = useState("");
  const [campaignContent, setCampaignContent] = useState("");
  const [selectedChannel, setSelectedChannel] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] = useState<any>(null);
  const { toast } = useToast();

  const handleGenerateContent = async () => {
    if (!campaignTitle.trim() || !campaignContent.trim() || !selectedChannel) {
      return;
    }

    setIsGenerating(true);
    
    // Simulate AI content generation
    await new Promise(resolve => setTimeout(resolve, 2500));
    
    const mockContent = {
      postText: `🚀 Descoperă cum poți să-ți crești afacerea cu soluții inovatoare!\n\n${campaignContent}\n\n💡 Află mai multe despre cum te putem ajuta să ajungi la următorul nivel.\n\n#business #antreprenoriat #moldova #success`,
      imageUrl: "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=500&h=300&fit=crop",
      dmMessage: `Salut! Am văzut că ești activ în comunitatea antreprenorilor. ${campaignContent} Te-ar interesa să colaborăm pentru a-ți crește vizibilitatea? Hai să discutăm! 😊`,
      scheduledFor: "Mâine la 10:00"
    };

    setGeneratedContent(mockContent);
    setIsGenerating(false);
  };

  const handleApprove = () => {
    toast({
      title: "Campanie aprobată!",
      description: "Campania ta a fost aprobată și va fi lansată conform programării.",
    });
  };

  const handleEdit = () => {
    toast({
      title: "Editare activată",
      description: "Poți modifica conținutul generat și să îl salvezi din nou.",
    });
  };

  const handleSchedule = () => {
    toast({
      title: "Campanie programată!",
      description: "Campania ta a fost programată pentru lansare automată.",
    });
  };

  if (generatedContent) {
    return (
      <div className="max-w-4xl mx-auto p-6 space-y-8 animate-fade-in">
        <div className="text-center space-y-4">
          <div className="flex justify-center">
            <div className="w-16 h-16 rounded-full gradient-bg flex items-center justify-center">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gradient">
            Conținut Generat cu Succes!
          </h1>
          <p className="text-lg text-muted-foreground">
            AI-ul a creat conținutul personalizat pentru campania ta "{campaignTitle}"
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Post Preview */}
          <Card className="card-hover">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MessageSquare className="w-5 h-5" />
                <span>Postarea Generată</span>
              </CardTitle>
              <CardDescription>
                Preview pentru {selectedChannel}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-secondary p-4 rounded-lg">
                <div className="whitespace-pre-line text-sm">
                  {generatedContent.postText}
                </div>
              </div>
              
              <div className="relative">
                <img 
                  src={generatedContent.imageUrl} 
                  alt="Generated content" 
                  className="w-full h-48 object-cover rounded-lg"
                />
                <Badge className="absolute top-2 right-2 bg-primary">
                  AI Generated
                </Badge>
              </div>

              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <Calendar className="w-4 h-4" />
                <span>Programat pentru: {generatedContent.scheduledFor}</span>
              </div>
            </CardContent>
          </Card>

          {/* DM Message */}
          <Card className="card-hover">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <MessageSquare className="w-5 h-5" />
                <span>Mesaj DM pentru Influenceri</span>
              </CardTitle>
              <CardDescription>
                Mesaj personalizat pentru outreach
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="bg-secondary p-4 rounded-lg">
                <div className="text-sm">
                  {generatedContent.dmMessage}
                </div>
              </div>
              
              <div className="mt-4 text-sm text-muted-foreground">
                💡 Mesajul poate fi personalizat pentru fiecare influencer
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Action Buttons */}
        <Card>
          <CardHeader>
            <CardTitle>Acțiuni pentru Campanie</CardTitle>
            <CardDescription>
              Alege ce vrei să faci cu conținutul generat
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4">
              <Button 
                onClick={handleApprove}
                className="gradient-bg hover:opacity-90 h-12"
              >
                <Check className="w-5 h-5 mr-2" />
                ✅ Aprobă
              </Button>
              
              <Button 
                onClick={handleEdit}
                variant="outline"
                className="h-12"
              >
                <Edit className="w-5 h-5 mr-2" />
                ✏️ Editează
              </Button>
              
              <Button 
                onClick={handleSchedule}
                variant="secondary"
                className="h-12"
              >
                <Calendar className="w-5 h-5 mr-2" />
                📅 Programează
              </Button>
            </div>
          </CardContent>
        </Card>

        <div className="text-center">
          <Button 
            variant="outline"
            onClick={() => setGeneratedContent(null)}
            className="mr-4"
          >
            Creează o Campanie Nouă
          </Button>
          <Button 
            className="gradient-bg hover:opacity-90"
            onClick={() => window.location.href = '/explorare'}
          >
            Înapoi la Explorarea Pieței
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-8 animate-fade-in">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold text-gradient">
          Lansează o Campanie
        </h1>
        <p className="text-xl text-muted-foreground">
          Creează conținut de marketing personalizat cu ajutorul AI-ului
        </p>
      </div>

      <Card className="card-hover">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5" />
            <span>Detalii Campanie</span>
          </CardTitle>
          <CardDescription>
            Completează informațiile pentru a genera conținut personalizat
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="title">Titlul campaniei *</Label>
            <Input
              id="title"
              value={campaignTitle}
              onChange={(e) => setCampaignTitle(e.target.value)}
              placeholder="ex: Promovare servicii de consultanță business"
              className="bg-secondary border-border"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="content">Ce vrei să promovezi? *</Label>
            <Textarea
              id="content"
              value={campaignContent}
              onChange={(e) => setCampaignContent(e.target.value)}
              placeholder="Descrie serviciul/produsul pe care vrei să îl promovezi, beneficiile pentru clienți, oferte speciale..."
              className="bg-secondary border-border min-h-[120px]"
              maxLength={300}
            />
            <div className="text-sm text-muted-foreground text-right">
              {campaignContent.length}/300
            </div>
          </div>

          <div className="space-y-2">
            <Label>Canal de promovare *</Label>
            <Select value={selectedChannel} onValueChange={setSelectedChannel}>
              <SelectTrigger className="bg-secondary border-border">
                <SelectValue placeholder="Alege canalul de promovare" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="facebook">Facebook</SelectItem>
                <SelectItem value="instagram">Instagram</SelectItem>
                <SelectItem value="grupuri">Grupuri Facebook</SelectItem>
                <SelectItem value="influenceri">Colaborare cu Influenceri</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {isGenerating ? (
            <div className="text-center space-y-4 py-8">
              <div className="flex justify-center">
                <div className="w-16 h-16 rounded-full gradient-bg flex items-center justify-center animate-pulse-soft">
                  <Sparkles className="w-8 h-8 text-white" />
                </div>
              </div>
              <div className="space-y-2">
                <h3 className="text-lg font-semibold">Generăm conținutul...</h3>
                <p className="text-muted-foreground">
                  AI-ul creează text, imagine și strategie personalizată
                </p>
                <div className="w-full bg-secondary rounded-full h-2 overflow-hidden">
                  <div className="h-full gradient-bg animate-pulse" style={{ width: '60%' }}></div>
                </div>
              </div>
            </div>
          ) : (
            <Button
              onClick={handleGenerateContent}
              disabled={!campaignTitle.trim() || !campaignContent.trim() || !selectedChannel}
              className="w-full gradient-bg hover:opacity-90 h-12 text-lg font-semibold"
            >
              <Sparkles className="w-5 h-5 mr-2" />
              Generează conținut
            </Button>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Campaigns;
