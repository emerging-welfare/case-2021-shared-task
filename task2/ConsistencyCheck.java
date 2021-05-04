package case2021.sharedtask.task2;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set; 
import java.util.StringTokenizer;

/**
 * This script checks the consistency of a system response and returns 
 * any potential errors. It takes as an argument a path to the file
 * with system response.
 * 
 * @author 
 *
 */

public class ConsistencyCheck {
	
	  public static List<String> FileToStringList(String fileName, String inputCharacterSet) throws IOException
		{ ArrayList<String> data;
		  String line;
		  data = new ArrayList<String>();	  
	 	  BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(fileName),inputCharacterSet));
		  while(true)
		    { if((line = in.readLine())==null) break;	      
		      line = line.trim();	        
		      data.add(line);
		    }
		   in.close(); 
	 	   return data;		   
		}
	
	 private static HashSet<String> eventTypes;
	 
	 static {
		 
		 eventTypes = new HashSet<String>();
		 
		 eventTypes.add("ABDUCT_DISSAP");
		 eventTypes.add("AGREEMENT");
		 eventTypes.add("AIR_STRIKE");
		 eventTypes.add("ARMED_CLASH");
		 eventTypes.add("ARREST");
		 eventTypes.add("ART_MISS_ATTACK");
		 eventTypes.add("ATTACK");
		 eventTypes.add("CHANGE_TO_GROUP_ACT");
		 eventTypes.add("CHEM_WEAP");
		 eventTypes.add("DISR_WEAP");
		 eventTypes.add("FORCE_AGAINST_PROTEST");
		 eventTypes.add("GOV_REGAINS_TERIT");
		 eventTypes.add("GRENADE");
		 eventTypes.add("HQ_ESTABLISHED");
		 eventTypes.add("MOB_VIOL");
		 eventTypes.add("NON_STATE_ACTOR_OVERTAKES_TER");
		 eventTypes.add("NON_VIOL_TERRIT_TRANSFER");
		 eventTypes.add("OTHER");
		 eventTypes.add("PEACE_PROTEST");
		 eventTypes.add("PROPERTY_DISTRUCT");
		 eventTypes.add("PROTEST_WITH_INTER");
		 eventTypes.add("REM_EXPLOS");
		 eventTypes.add("SEX_VIOL");
		 eventTypes.add("SUIC_BOMB");
		 eventTypes.add("VIOL_DEMONSTR");
		 eventTypes.add("ORG_CRIME");
		 eventTypes.add("NATURAL_DISASTER");
		 eventTypes.add("MAN_MADE_DISASTER");		 
		 eventTypes.add("ATTRIB");
		 eventTypes.add("DIPLO");		 
		 
}
	  
	 public static void main(String[] args) throws IOException
		{ String inputFile = args[0];	   
		  List<String> lines = FileToStringList(inputFile,"UTF-8");
		  HashMap<String,Integer> countTypes = new HashMap<String,Integer>(); 
		  HashSet<String> errors = new HashSet<String>();
		  HashSet<Integer> uniqueIDs = new HashSet<Integer>();
          for(String s : eventTypes)
        	 countTypes.put(s, 0); 
		  for(int i = 0;i<lines.size();i++)
           { String next = lines.get(i);
             if(next.length()==0)
               continue;	 
		     StringTokenizer st = new StringTokenizer(next,"\t");
		     if(st.countTokens()!=2)
		      { errors.add("WRONG NUMBER OF ELEMENTS IN LINE: " + i + ":> " + next);
		        continue;
		      }	 
		     String id = st.nextToken();
		     String type = st.nextToken();
		     int index;
		     try { index = Integer.parseInt(id);
		         }
		     catch(Exception e)
		      { errors.add("ID: " + id + " IS NOT AN INTEGER IN LINE: " + i + ":> " + next);
		        continue;
		      }	 
		     if(uniqueIDs.contains(index))
		       { errors.add("ID: " + id + " IS NOT UNIQUE IN LINE: " + i + ":> " + next); } 
		     else
		      uniqueIDs.add(index);	 
		     if(!eventTypes.contains(type))
		      { errors.add("INVALID EVENT TYPE: '" + type + "' IN LINE: " + i + ":> " + next);
		        continue;
		      }	 
		     int count = countTypes.get(type);
		     countTypes.put(type, count + 1);		       	 		       
		 }
		if(errors.size()==0)
		  System.out.println("NO ERRORS FOUND");	
		else
		 { System.out.println("FOLLOWING ERRORS FOUND:");
		   for(String s : errors)
			  System.out.println(s); 
		 }
		if(errors.size()==0)
		 { System.out.println("EVENT TYPE STATISTICS:");  
		   Set<String> types = countTypes.keySet();
		   for(String t : types)
		     System.out.println(t + ": " + countTypes.get(t));
		 }  
	  } 
}
