package org.styfi.model;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.URL;

import org.styfi.servlets.ImageUpload;

public class DataController {
	public static boolean DEBUG = false;
	public static String INSTANCE = "aws";
	
	public void setDebug(boolean debug) {
		DEBUG = debug;
	}
	
	public void setInstance(String instance) {
		INSTANCE = instance;
	}
	

	public String return_best (String timeStamp, String image_path, PrintWriter out) throws IOException {
		/* >>>>>>>> FIND THE RELATIVE PATH <<<<<<< */
		URL location = ImageUpload.class.getProtectionDomain().getCodeSource().getLocation();
	    String path = location.getPath();
	    path = path.substring(0,path.length() - 16);
		
	    /* >>>>>>>> DEBUG? <<<<<<< */
		@SuppressWarnings("unused")
		String debugString = "Input:" + "\n";
		if(DEBUG) out.println(path); 

		String response = "";
		/* >>>>>>>> EXECUTE BASH SCRIPT WHICH RUNS DIRECTLY ON THE DEFINED MACHINE <<<<<<< */	
	    String line;
        Process p;
		try {
			/* >>>>>>>> EXECUTE THE SCRIPT RUNNING SEARCHENGINE.PY <<<<<<< */
			/* >>>>>>>> ON THE REMOTE AWS SERVER <<<<<<<  */
			if(INSTANCE == "aws") {
				p = new ProcessBuilder("/home/ubuntu/git_repos/styfi_dir_on_server/bash_script_local.sh" , "/home/ubuntu/git_repos/cv-sift-search/" + timeStamp + ".jpg", timeStamp).start();
			}
			/* >>>>>>>> LOCALLY <<<<<<<  */
			else {
	        	p = new ProcessBuilder("/users/irausch/git_repos/styfi_dir_on_server/bash_script_local.sh" , "/users/irausch/git_repos/cv-sift-search/" + timeStamp + ".jpg", timeStamp).start();
			}
            
        	// >>>>>>>> READ THE OUTPUT = SEARCHENGINE RESULTS <<<<<<<
        	BufferedReader br = new BufferedReader(
                new InputStreamReader(p.getInputStream()));
            while ((line = br.readLine()) != null){
                debugString += line + "\n";
                response += line + "\n";
            }
            
            // >>>>>>>> DEBUG <<<<<<<
            if(DEBUG){
	            out.println(debugString);
	            debugString += "Error: " + "\n";
	        	BufferedReader errorReader = new BufferedReader(
		                new InputStreamReader(p.getErrorStream()));
		            while ((line = errorReader.readLine()) != null){
		                debugString += line + "\n";
		            }
		        out.println(debugString);
            }
            // >>>>>>>> waitFor() causes the current thread to wait, if necessary, until the process represented by this Process object has terminated. <<<<<<<
            p.waitFor();
            
        } catch (Exception e) { out.println(e);}
		
		//out.println(response);
			
		return response;
	}

}
