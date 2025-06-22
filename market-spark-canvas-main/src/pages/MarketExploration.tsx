import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Facebook, Users, Calendar, Star, Plus, ArrowRight } from "lucide-react";

const MarketExploration = () => {
 const [addedToPlan, setAddedToPlan] = useState([]);

 const showToast = (title, description) => {
   console.log(`${title}: ${description}`);
 };

 const marketData = {
   facebookGroups: [
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
   ],
   influencers: [
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
   ],
   events: [
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
   ]
 };

 const handleAddToPlan = (id, type, title) => {
   if (addedToPlan.includes(id)) return;
   
   setAddedToPlan(prev => [...prev, id]);
   showToast("Adăugat în plan!", `${title} a fost adăugat în planul tău de marketing.`);
 };

 const renderStars = (score) => (
   <div className="flex items-center space-x-1">
     {[...Array(5)].map((_, i) => (
       <Star 
         key={i} 
         className={`w-4 h-4 ${i < score ? "text-yellow-400 fill-current" : "text-gray-300"}`}
       />
     ))}
     <span className="text-sm text-gray-500 ml-1">({score}/5)</span>
   </div>
 );

 const MarketingCard = ({ item, type, icon: IconComponent, iconColor }) => {
   const isAdded = addedToPlan.includes(item.id);
   
   return (
     <Card className="border border-gray-200 hover:shadow-lg transition-all duration-200 group">
       <CardHeader>
         <div className="flex items-start justify-between">
           <CardTitle className="text-lg text-gray-800 group-hover:text-blue-600 transition-colors">
             {item.title}
           </CardTitle>
           {item.category && (
             <Badge variant="secondary" className="bg-gray-100 text-gray-700">
               {item.category}
             </Badge>
           )}
         </div>
         <CardDescription className="text-gray-600 leading-relaxed">
           {item.description}
         </CardDescription>
       </CardHeader>
       <CardContent className="space-y-4">
         <div className="grid grid-cols-2 gap-4 text-sm">
           {item.members && (
             <>
               <div>
                 <span className="text-gray-500">Membri:</span>
                 <div className="font-semibold text-gray-800">{item.members}</div>
               </div>
             </>
           )}
           {item.followers && (
             <>
               <div>
                 <span className="text-gray-500">Followeri:</span>
                 <div className="font-semibold text-gray-800">{item.followers}</div>
               </div>
               <div>
                 <span className="text-gray-500">Engagement:</span>
                 <div className="font-semibold text-green-600">{item.engagement}</div>
               </div>
             </>
           )}
           {item.date && (
             <>
               <div>
                 <span className="text-gray-500">Data:</span>
                 <div className="font-semibold text-gray-800">{item.date}</div>
               </div>
               <div>
                 <span className="text-gray-500">Participanți:</span>
                 <div className="font-semibold text-blue-600">{item.attendees}</div>
               </div>
             </>
           )}
         </div>
         
         <div className="space-y-2">
           <span className="text-sm text-gray-500">Scor de Relevanță:</span>
           {renderStars(item.relevanceScore)}
         </div>
         
         <Button 
           onClick={() => handleAddToPlan(item.id, type, item.title)}
           disabled={isAdded}
           className={`w-full transition-all ${
             isAdded 
               ? "bg-green-100 text-green-700 hover:bg-green-100" 
               : "bg-blue-600 hover:bg-blue-700 text-white"
           }`}
         >
           {isAdded ? (
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
   );
 };

 const SectionHeader = ({ icon: IconComponent, iconColor, title }) => (
   <div className="flex items-center space-x-3 mb-6">
     <div className={`w-8 h-8 rounded-lg ${iconColor} flex items-center justify-center`}>
       <IconComponent className="w-5 h-5 text-white" />
     </div>
     <h2 className="text-2xl font-bold text-gray-800">{title}</h2>
   </div>
 );

 return (
   <div className="max-w-7xl mx-auto p-6 space-y-12">
     <div className="text-center space-y-4">
       <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
         Explorează Piața
       </h1>
       <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
         Am identificat cele mai relevante oportunități pentru afacerea ta. 
         Adaugă-le în planul de marketing pentru a începe să te conectezi cu clienții ideali.
       </p>
     </div>

     <div className="space-y-12">
       <section>
         <SectionHeader 
           icon={Facebook} 
           iconColor="bg-blue-500" 
           title="Grupuri Facebook Recomandate" 
         />
         <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
           {marketData.facebookGroups.map((group) => (
             <MarketingCard 
               key={group.id}
               item={group} 
               type="group" 
               icon={Facebook}
               iconColor="text-blue-500"
             />
           ))}
         </div>
       </section>

       <section>
         <SectionHeader 
           icon={Users} 
           iconColor="bg-purple-500" 
           title="Influenceri Locali Recomandați" 
         />
         <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
           {marketData.influencers.map((influencer) => (
             <MarketingCard 
               key={influencer.id}
               item={influencer} 
               type="influencer" 
               icon={Users}
               iconColor="text-purple-500"
             />
           ))}
         </div>
       </section>

       <section>
         <SectionHeader 
           icon={Calendar} 
           iconColor="bg-cyan-500" 
           title="Evenimente Locale Relevante" 
         />
         <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
           {marketData.events.map((event) => (
             <MarketingCard 
               key={event.id}
               item={event} 
               type="event" 
               icon={Calendar}
               iconColor="text-cyan-500"
             />
           ))}
         </div>
       </section>
     </div>

     {addedToPlan.length > 0 && (
       <div className="text-center pt-8">
         <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-8 border border-blue-200"></div>
           <h3 className="text-lg font-semibold text-gray-800 mb-4">
             Planul tău de marketing este gata!
           </h3>
           <p className="text-gray-600 mb-6">
             Ai selectat {addedToPlan.length} oportunități pentru a-ți promova afacerea.
           </p>
           <Button 
             size="lg" 
             className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-4 text-lg font-semibold shadow-lg"
           >
             Continuă cu Campaniile
             <ArrowRight className="ml-2 w-5 h-5" />
           </Button>
         </div>
       </div>
     )}
   </div>
 );
};

export default MarketExploration;
