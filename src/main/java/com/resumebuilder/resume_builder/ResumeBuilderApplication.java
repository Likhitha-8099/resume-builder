package com.resumebuilder.resume_builder;

import java.io.File;
import java.nio.file.Files;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class ResumeBuilderApplication {

	public static void main(String[] args) {
		loadDotEnv();
		SpringApplication.run(ResumeBuilderApplication.class, args);
	}

	private static void loadDotEnv() {
		try {
			File envFile = new File(".env");
			if (!envFile.exists()) {
				envFile = new File("../.env");
			}
			if (envFile.exists()) {
				Files.lines(envFile.toPath()).forEach(line -> {
					String trimmed = line.trim();
					if (!trimmed.isEmpty() && !trimmed.startsWith("#") && trimmed.contains("=")) {
						int idx = trimmed.indexOf("=");
						String key = trimmed.substring(0, idx).trim();
						String value = trimmed.substring(idx + 1).trim();
						if (System.getProperty(key) == null && System.getenv(key) == null) {
							System.setProperty(key, value);
						}
					}
				});
			}
		} catch (Exception ignored) {
		}
	}

}

