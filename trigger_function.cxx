#include <TH1F.h>
#include <TFile.h>
double trigger_function(double htJet30=700) {
   double result;
// open a file and get a histogram
   
//   cout << histo->GetName() << endl;
//   cout << histo->GetBinContent(htJet30) << endl;
   result = histo_efficiency->GetBinContent(htJet30);
//   cout << result << endl;
//   f->Close();
   return result;    
   
   
}


#include <TH1F.h>
#include <TFile.h>
double trigger_function_lower(double htJet30=700) {
   double result;
// open a file and get a histogram
   
//   cout << histo->GetName() << endl;
//   cout << histo->GetBinContent(htJet30) << endl;
   result = histo_efficiency_lower->GetBinContent(htJet30);
//   cout << result << endl;
//   f->Close();
   return result;    
   
   
}


#include <TH1F.h>
#include <TFile.h>
double trigger_function_upper(double htJet30=700) {
   double result;
// open a file and get a histogram
   
//   cout << histo->GetName() << endl;
//   cout << histo->GetBinContent(htJet30) << endl;
   result = histo_efficiency_upper->GetBinContent(htJet30);
//   cout << result << endl;
//   f->Close();
   return result;    
   
   
}


