import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.util.Iterator;

import com.demo.glucoseAppClass;
import com.mathworks.toolbox.javabuilder.MWException;
import com.mathworks.toolbox.javabuilder.external.org.json.JSONException;
import com.mathworks.toolbox.javabuilder.external.org.json.JSONObject;



 class Main {
	
	
	/**
	 * @param args
	 * @throws MWException 
	 */
	public static void main(String[] args) throws MWException {
		//Variable declarations
		double mealCHO = 0.0; //weighted carb serving for each meal
		double carb_p_serv_double = 0.0;
		double num_servings_double = 0.0; 
		// JSON PARSERS
		try {
			JSONObject reader = new JSONObject(readUrl("http://198.61.177.186:8080/virgil/data/glucoseapp/menu/1"));
			
			Iterator<?> keys = reader.keys();
			
			while (keys.hasNext()){
				
				String currentTimestamp = (String) keys.next();
				
				String menuItem = reader.getString(currentTimestamp);
				JSONObject currentMenuObject = new JSONObject(menuItem);
				String carb_p_serv = currentMenuObject.getString("carb_p_serv");
				String num_servings = currentMenuObject.getString("num_servings");
				String g_load = currentMenuObject.getString("g_load");
				
				System.out.println(carb_p_serv);
				System.out.println(num_servings);
				System.out.println(g_load);
				
				carb_p_serv_double = Double.parseDouble(carb_p_serv);
				num_servings_double = Double.parseDouble(num_servings);
				mealCHO += carb_p_serv_double*num_servings_double;
				} 
			}
			catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (JSONException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		
		glucoseAppClass c = null;
		Object[] result = null;
		
		// Create test modelData array
		Double data[] = new Double[] {70.0,7.0,0.0,mealCHO,0.0,13.0,0.0,0.0,0.0,18.0,0.0,0.0,0.0,30.0,1.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0};
			
		//Create new glucose App Class
		c = new glucoseAppClass();
			
		//Call GUISimulateCobelliDay function
		result = c.GUISimulateCobelliDay(3,(Object)data);
			
		System.out.println(result[1]);
			
		


	}
	
	private static String readUrl(String urlString) throws Exception {
	    BufferedReader reader = null;
	    try {
	        URL url = new URL(urlString);
	        reader = new BufferedReader(new InputStreamReader(url.openStream()));
	        StringBuffer buffer = new StringBuffer();
	        int read;
	        char[] chars = new char[1024];
	        while ((read = reader.read(chars)) != -1)
	            buffer.append(chars, 0, read); 

	        return buffer.toString();
	    } finally {
	        if (reader != null)
	            reader.close();
	    }
	}
	
}
