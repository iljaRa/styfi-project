package org.styfi.servlets;

import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.PrintWriter;
import java.io.Serializable;
import java.net.URL;
import java.nio.file.Files;
import java.text.SimpleDateFormat;
import java.util.Base64;
import java.util.Calendar;
import java.util.LinkedList;

import javax.imageio.ImageIO;
import javax.servlet.ServletException;
import javax.servlet.ServletInputStream;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.styfi.model.DataController;
import org.styfi.model.DataPreparation;
import org.styfi.model.Item;

/**
 * Servlet implementation class ImageUpload.
 */
@WebServlet("/ImageUpload")
public class ImageUpload extends HttpServlet {
	private static final long serialVersionUID = 1L;
	public static boolean RECORD_TIME = true;
	public static boolean DEBUG = false;
	public static String INSTANCE = "ilja";

	public void setDebug(boolean debug) {
		DEBUG = debug;
	}

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		/* >>>>>>>> INITIALIZE <<<<<<< */
		long startTime = System.currentTimeMillis();

		long overallTime = 0;
		response.setContentType("text/html");
		PrintWriter out = response.getWriter();

		ServletInputStream is = request.getInputStream();

		ByteArrayOutputStream buffer = new ByteArrayOutputStream();

		int nRead;
		byte[] data = new byte[16384];

		while ((nRead = is.read(data, 0, data.length)) != -1) {
			buffer.write(data, 0, nRead);
		}

		/* >>>>>>>> FIND THE RELATIVE PATH <<<<<<< */
		//URL location = ImageUpload.class.getProtectionDomain().getCodeSource().getLocation();
		//String path = location.getPath();
		//String path_dir = path.substring(0, path.length() - 16);
		//path = path_dir + "byteImg";
		// out.println(path);

		long endTime = System.currentTimeMillis();

		if (RECORD_TIME) {
			out.println("TIME: Misc took " + (endTime - startTime) + " milliseconds");
			overallTime += (endTime - startTime);
			startTime = System.currentTimeMillis();
		}

		/* >>>>>>>> READ IN THE IMAGE <<<<<<< */

		String homeDir = "";

		switch (INSTANCE) {
		case "ilja":
			homeDir = "/home/ilja";
			break;
		case "aws":
			homeDir = "/home/ubuntu";
			break;
		case "other":
			homeDir = "/users/irausch";
			break;
		default:
			System.out.println("WE SHOULD NOT BE HERE. CHECKOUT THE home dir.");
		}
		

		String timeStamp = new SimpleDateFormat("yyyy_MM_dd_HH_mm_ss_SS").format(Calendar.getInstance().getTimeInMillis());

		String image_path = homeDir + "/git_repos/cv-sift-search/" + timeStamp + ".jpg";
		File image = new File(image_path);

		try {
			ByteArrayInputStream bIn = new ByteArrayInputStream(buffer.toByteArray());
			BufferedImage bIm = ImageIO.read(bIn);
			ImageIO.write(bIm, "jpg", image);
		} catch (Exception e) {
			out.print(e.getLocalizedMessage());
		}
		if (RECORD_TIME) {
			endTime = System.currentTimeMillis();
			out.println("TIME: Reading the image took " + (endTime - startTime) + " milliseconds");
			overallTime += (endTime - startTime);
			startTime = System.currentTimeMillis();
		}

		/* >>>>>>>> FIND MATCHES <<<<<<< */

		DataController dC = new DataController();
		dC.setDebug(DEBUG);
		dC.setInstance(INSTANCE);
		
		String best_results = dC.return_best(timeStamp, image_path, out);
		
		try {
			boolean imageDeleted = Files.deleteIfExists(image.toPath());
			if(!imageDeleted && DEBUG) out.println(image_path);
		} catch (Exception e) {
			out.print(e.getLocalizedMessage());
		}
		
		if (RECORD_TIME) {
			endTime = System.currentTimeMillis();
			out.println("TIME: Finding matches took " + (endTime - startTime) + " milliseconds");
			overallTime += (endTime - startTime);
			startTime = System.currentTimeMillis();
		}

		/* >>>>>>>> RETRIEVE DATA FROM DB <<<<<<< */

		String[] t_shirt_id_array = best_results.split("\n");
		LinkedList<Item> items = new LinkedList<Item>();
		DataPreparation dP = new DataPreparation();
		dP.setDebug(DEBUG);

		for (String t_shirt_id : t_shirt_id_array) {
			try {
				items.add(dP.get_item_by_id(t_shirt_id, out));
				if (DEBUG) out.println("DB received item: " + t_shirt_id + "\n");
			} catch (Exception e) {
				out.print(e.getLocalizedMessage());
			}

		}

		if (RECORD_TIME) {
			endTime = System.currentTimeMillis();
			out.println("TIME: Retrieving data from DB took " + (endTime - startTime) + " milliseconds");
			overallTime += (endTime - startTime);
			startTime = System.currentTimeMillis();
		}

		/*
		 * out.print("Length item list: " + t_shirt_id_array.length + "\n");
		 * out.print("Der beste Treffer ist das Produkt " + items.get(0).getItem_name())
		 * ; out.print(" welches in " + items.get(0).getShop()) ;
		 * out.print(" erhaeltlich ist fuer " + items.get(0).getPrice() );
		 * out.print("Euro.\n"); out.print("URL: " + items.get(0).getUrl() + "\n");
		 * //out.print("Image Path: " + items.get(0).getImage_path() + "\n");
		 */

		/* >>>>>>>> OUTPUT BEST MATCHES AS BYTE ARRAYS <<<<<<< */
		if (!DEBUG && !RECORD_TIME) out.write(toString(items));

		if (RECORD_TIME) {
			endTime = System.currentTimeMillis();
			out.println("TIME: Printing + sending results took " + (endTime - startTime) + " milliseconds");
			overallTime += (endTime - startTime);
			out.println("TIME: Overall, the app took " + overallTime + " milliseconds");
		}

		/* >>>>>>>> CLOSE <<<<<<< */
		dP.finalize();
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		System.out.println("post");
		doGet(request, response);
	}

	/** Read the object from Base64 string. */
	@SuppressWarnings("unused")
	private static Object fromString(String s) throws IOException, ClassNotFoundException {
		byte[] data = Base64.getDecoder().decode(s);
		ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
		Object o = ois.readObject();
		ois.close();
		return o;
	}

	/** Write the object to a Base64 string. */
	private static String toString(Serializable o) throws IOException {
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		ObjectOutputStream oos = new ObjectOutputStream(baos);
		oos.writeObject(o);
		oos.close();
		return Base64.getEncoder().encodeToString(baos.toByteArray());
	}

}
