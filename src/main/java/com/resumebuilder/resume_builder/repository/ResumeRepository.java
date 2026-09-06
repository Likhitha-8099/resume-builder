package com.resumebuilder.resume_builder.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.resumebuilder.resume_builder.model.Resume;


@Repository
public interface ResumeRepository extends JpaRepository<Resume,Long>{

}
