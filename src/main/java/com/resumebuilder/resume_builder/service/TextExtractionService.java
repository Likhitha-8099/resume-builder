package com.resumebuilder.resume_builder.service;

import java.io.InputStream;
import org.apache.pdfbox.Loader;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class TextExtractionService {

    private static final Logger logger = LoggerFactory.getLogger(TextExtractionService.class);

    public String extractTextFromPdf(MultipartFile file, String fileDescription) {
        if (file == null || file.isEmpty()) {
            throw new IllegalArgumentException(fileDescription + " file is missing or empty.");
        }

        String originalFilename = file.getOriginalFilename();
        if (originalFilename != null && !originalFilename.toLowerCase().endsWith(".pdf")) {
            throw new IllegalArgumentException(fileDescription + " must be a PDF file.");
        }

        logger.info("[JOB-FIT] " + fileDescription + " extraction started: " + originalFilename);

        try (InputStream inputStream = file.getInputStream();
             PDDocument document = Loader.loadPDF(inputStream.readAllBytes())) {

            PDFTextStripper stripper = new PDFTextStripper();
            String text = stripper.getText(document);

            if (text == null || text.trim().isEmpty()) {
                throw new IllegalArgumentException(fileDescription + " PDF contains no readable text.");
            }

            String trimmedText = text.trim();
            logger.info("[JOB-FIT] " + fileDescription + " extraction completed. Character count: " + trimmedText.length());
            return trimmedText;

        } catch (IllegalArgumentException ex) {
            throw ex;
        } catch (Exception ex) {
            logger.error("[JOB-FIT] Failed to extract text from " + fileDescription + ": " + ex.getMessage(), ex);
            throw new RuntimeException("Unable to read " + fileDescription + " PDF: " + ex.getMessage());
        }
    }
}
