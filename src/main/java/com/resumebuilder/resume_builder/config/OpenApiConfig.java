package com.resumebuilder.resume_builder.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
@Configuration

public class OpenApiConfig {
	
	
	  @Bean
	    public OpenAPI resumeBuilderOpenAPI() {
	        return new OpenAPI()
	                .info(new Info()
	                        .title("AI Resume Builder API")
	                        .description("Backend APIs for AI-powered resume creation, resume CRUD, and AI summary generation")
	                        .version("1.0.0"));
	    }

}
