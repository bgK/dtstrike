package six.challenge.localtester;

import java.awt.Desktop;
import java.awt.EventQueue;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintStream;
import java.util.InvalidPropertiesFormatException;
import java.util.Properties;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.JTextPane;
import javax.swing.filechooser.FileNameExtensionFilter;

import net.miginfocom.swing.MigLayout;
import six.challenge.engine.Engine;

public class MainWindows {

	private JFrame frmSixchallengeLocaltester;
	private JTextField mapField;
	private JTextField bot1Field;
	private JButton btnOpenFile;
	private JButton btnNewButton;
	private JLabel lblBot;
	private JTextField bot2Field;
	private JLabel lblBot_1;
	private JTextField bot3Field;
	private JLabel lblBot_2;
	private JTextField bot4Field;
	private JLabel lblBot_3;
	private JButton btnStart;
	private JLabel lblLocalLauncher;
	private JLabel lblNombreDeTours;
	private JTextField turnsField;
	private JLabel lblMillisecondesParT;
	private JTextField timeField;
	private JTextPane errorPane;
	private JScrollPane scrollPane;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					MainWindows window = new MainWindows();
					window.frmSixchallengeLocaltester.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public MainWindows() {
		initialize();
		
		// Restore fields values
		Properties probLib = new Properties();
		try {
			File propFile = new File("props.xml");
			FileInputStream reader =new FileInputStream(propFile);
			probLib.loadFromXML(reader);
			
			// Restore
			mapField.setText(probLib.getProperty("map", ""));
			bot1Field.setText(probLib.getProperty("bot1", ""));
			bot2Field.setText(probLib.getProperty("bot2", ""));
			bot3Field.setText(probLib.getProperty("bot3", ""));
			bot4Field.setText(probLib.getProperty("bot4", ""));
			turnsField.setText(probLib.getProperty("turns", turnsField.getText()));
			timeField.setText(probLib.getProperty("time", timeField.getText()));
			
		} catch (FileNotFoundException e) {
			// No properties
		} catch (InvalidPropertiesFormatException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {

		frmSixchallengeLocaltester = new JFrame();
		frmSixchallengeLocaltester.setTitle("SixChallenge LocalTester");
		frmSixchallengeLocaltester.setBounds(100, 100, 650, 425);
		frmSixchallengeLocaltester.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frmSixchallengeLocaltester.getContentPane().setLayout(new MigLayout("", "[grow]", "[][][][][][][][][][grow]"));

		lblLocalLauncher = new JLabel("Local Launcher ");
		frmSixchallengeLocaltester.getContentPane().add(lblLocalLauncher, "cell 0 0");

		JLabel lblSelectionDeLa = new JLabel("Map Selection: ");
		frmSixchallengeLocaltester.getContentPane().add(lblSelectionDeLa, "flowx,cell 0 1");

		mapField = new JTextField();
		frmSixchallengeLocaltester.getContentPane().add(mapField, "cell 0 1,growx");
		mapField.setColumns(10);

		lblBot = new JLabel("Bot 1 : ");
		frmSixchallengeLocaltester.getContentPane().add(lblBot, "flowx,cell 0 2");

		bot1Field = new JTextField();
		frmSixchallengeLocaltester.getContentPane().add(bot1Field, "cell 0 2,growx");
		bot1Field.setColumns(10);

		btnOpenFile = new JButton("Open Map");
		btnOpenFile.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				String choosenMap = chooseMap();
				// TODO open file to check it's fine
				// TODO récupérer le nom qualifié complet
				// TODO si pas de selection, ne pas écraser
				mapField.setText(choosenMap);
			}
		});
		frmSixchallengeLocaltester.getContentPane().add(btnOpenFile, "cell 0 1");

		btnNewButton = new JButton("Select bots");
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				BotLibrary dialog = new BotLibrary();
				try {
					dialog.showOpenDialog(bot1Field,bot2Field,bot3Field,bot4Field);
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}

			}
		});
		frmSixchallengeLocaltester.getContentPane().add(btnNewButton, "cell 0 2");

		lblBot_1 = new JLabel("Bot 2 : ");
		frmSixchallengeLocaltester.getContentPane().add(lblBot_1, "flowx,cell 0 3");

		bot2Field = new JTextField();
		bot2Field.setColumns(10);
		frmSixchallengeLocaltester.getContentPane().add(bot2Field, "cell 0 3,growx");

		lblBot_2 = new JLabel("Bot 3 : ");
		frmSixchallengeLocaltester.getContentPane().add(lblBot_2, "flowx,cell 0 4");

		bot3Field = new JTextField();
		bot3Field.setColumns(10);
		frmSixchallengeLocaltester.getContentPane().add(bot3Field, "cell 0 4,growx");

		lblBot_3 = new JLabel("Bot 4 : ");
		frmSixchallengeLocaltester.getContentPane().add(lblBot_3, "flowx,cell 0 5");

		bot4Field = new JTextField();
		bot4Field.setColumns(10);
		frmSixchallengeLocaltester.getContentPane().add(bot4Field, "cell 0 5,growx");

		lblNombreDeTours = new JLabel("Max Number of turns");
		frmSixchallengeLocaltester.getContentPane().add(lblNombreDeTours, "flowx,cell 0 6");

		lblMillisecondesParT = new JLabel("Millisecondes per turn");
		frmSixchallengeLocaltester.getContentPane().add(lblMillisecondesParT, "flowx,cell 0 7");

		btnStart = new JButton("> Start");
		btnStart.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {

				StartSimulation(mapField.getText(), turnsField.getText(), timeField.getText(), bot1Field.getText(), bot2Field.getText(),
						bot3Field.getText(), bot4Field.getText());

			}
		});
		frmSixchallengeLocaltester.getContentPane().add(btnStart, "flowx,cell 0 8");

		turnsField = new JTextField();
		turnsField.setText("1000");
		frmSixchallengeLocaltester.getContentPane().add(turnsField, "cell 0 6,align right");
		turnsField.setColumns(10);

		timeField = new JTextField();
		timeField.setText("1000");
		frmSixchallengeLocaltester.getContentPane().add(timeField, "cell 0 7,align right");
		timeField.setColumns(10);
		
		scrollPane = new JScrollPane();
		frmSixchallengeLocaltester.getContentPane().add(scrollPane, "cell 0 9,grow");

		errorPane = new JTextPane();
		scrollPane.setViewportView(errorPane);
		errorPane.setAutoscrolls(true);

		frmSixchallengeLocaltester.addWindowListener(new WindowListener() {
			@Override
			public void windowOpened(WindowEvent e) {
			}
			@Override
			public void windowIconified(WindowEvent e) {
			}
			@Override
			public void windowDeiconified(WindowEvent e) {
			}
			@Override
			public void windowDeactivated(WindowEvent e) {
			}
			
			@Override
			public void windowClosing(WindowEvent e) {
				// Window closing, store pref
				Properties probLib = new Properties();
				probLib.put("map", mapField.getText());
				probLib.put("bot1", bot1Field.getText());
				probLib.put("bot2", bot2Field.getText());
				probLib.put("bot3", bot3Field.getText());
				probLib.put("bot4", bot4Field.getText());
				probLib.put("turns", turnsField.getText());
				probLib.put("time", timeField.getText());
				
				// Save file
				try {
					File propFile = new File("props.xml");
					FileOutputStream writer = new FileOutputStream(propFile);
					probLib.storeToXML(writer, "");
					writer.close();
				} catch (FileNotFoundException fnfe) {
					// No properties
				} catch (InvalidPropertiesFormatException ee) {
					ee.printStackTrace();
				} catch (IOException ee) {
					ee.printStackTrace();
				}
			}
			
			@Override
			public void windowClosed(WindowEvent e) {
			}
			@Override
			public void windowActivated(WindowEvent e) {
			}
		});
	}

	private String chooseMap() {
		File maps = new File("maps");
		JFileChooser chooser = new JFileChooser(maps);

		FileNameExtensionFilter filter = new FileNameExtensionFilter("Maps", "txt");
		chooser.setFileFilter(filter);

		// FileFilter
		int returnVal = chooser.showOpenDialog(frmSixchallengeLocaltester);

		if ((returnVal == JFileChooser.APPROVE_OPTION)) {
			return chooser.getSelectedFile().getAbsolutePath();
		}
		return null;
	}


	private boolean StartSimulation(String map, String maxTime, String nbTurns, String bot1, String bot2, String bot3, String bot4) {
		/*
		 * mapFile = args[0]; turntime = Integer.parseInt(args[1]); turns =
		 * Integer.parseInt(args[2]); logFile = args[3];
		 */

		File replayFolder = new File("replay");
		if (!replayFolder.exists()){
			replayFolder.mkdir();
		}
		String[] replays = replayFolder.list();
		int maxvalue = 0;
		try {
			for (int i=0;i<replays.length;i++){
				if (replays[i].startsWith("index")){
					int value=Integer.parseInt(replays[i].subSequence(5, 8).toString());
					if (value > maxvalue){
						maxvalue=value;
					}
				}
			}
		} catch (NumberFormatException e) {
		}
		maxvalue++;
		
		String runFolder = "tempDir";
		new File(runFolder).delete();
		new File(runFolder).mkdir();
		
		try {
			// Try to delete old log file
			new File(runFolder, "/log.txt").delete();
		} catch (Exception e) {
		}

		String[] params = null;
		if ("".equals(bot3)) {
			params = new String[] { map, maxTime, nbTurns, runFolder + "/log.txt", bot1, bot2 };
		} else if ("".equals(bot4)) {
			params = new String[] { map, maxTime, nbTurns, runFolder + "/log.txt", bot1, bot2, bot3 };
		} else {
			params = new String[] { map, maxTime, nbTurns, runFolder + "/log.txt", bot1, bot2, bot3, bot4 };
		}

		File errorLog = new File(runFolder + "/GameError.txt");

		PrintStream errorStream = null;
		try {
			errorLog.createNewFile();
			errorStream = new PrintStream(errorLog);
			System.setErr(errorStream);

		} catch (IOException e2) {
			e2.printStackTrace();
		}

		Engine engine = new Engine(params);

		if (!engine.errorAtStartup) {
			engine.play();
			String replayData = engine.end();
			File replay = null;
			try {
				replay = new File("replay/replay"+String.format("%03d", maxvalue)+".js");
				replay.createNewFile();
				FileWriter jswriter = new FileWriter(replay);
				jswriter.write("var replayJson=");
				jswriter.write(replayData);
				jswriter.flush();
				jswriter.close();

				replay = new File("replay/index"+String.format("%03d", maxvalue)+".html");
				replay.createNewFile();
				FileWriter indexWriter = new FileWriter(replay);
				File index  = new File("replay/inc/index.html"); 
				FileReader reader = new FileReader(index);
				StringBuilder line = new StringBuilder();
				int c;
				while ((c = reader.read()) >= 0) {
					line = line.append((char) c);
				}
				indexWriter.write(line.toString().replaceFirst("replay", "replay"+String.format("%03d", maxvalue)));
				indexWriter.flush();
				indexWriter.close();			
				reader.close();

				// open the default web browser for the HTML page
				Desktop.getDesktop().browse(replay.toURI());
				
				
			} catch (IOException e1) {
				displayErrorLog(errorLog);
			}

		} else {
			displayErrorLog(errorLog);

		}

		// cleanup
		if (errorStream != null) {
			errorStream.close();
		}
		engine = null;

		return true;

	}

	private void displayErrorLog(File errorLog) {
		try {
			FileReader reader = new FileReader(errorLog);
			StringBuilder line = new StringBuilder();
			int c;
			while ((c = reader.read()) >= 0) {
				line = line.append((char) c);
			}
			reader.close();
			errorPane.setText(line.toString());
			errorPane.requestFocus();

		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	}

}
