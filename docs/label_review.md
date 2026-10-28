# Label spot-check

For each query, read the passages listed as correct answers.
Tick `[x]` on a line only if that passage does NOT answer the query.
Leave the others as `[ ]`.
Then run: `uv run searchlab --corpus nasa apply-review`.

## n003 · exact_id · test

**Query:** NPR 7150.2D software engineering acronyms

- [ ] wrong · n003 · 236b02f03f8a7a8e · *6.2 Software Engineering Product Content* (p45)
  > NPR 7150.2D -- AppendixA Page 52 of 89 Appendix B. Acronyms CAD/CAM Computer-Aided Design/and Computer-Aided Manufacturing CE Chief Engineer CHMO Chief Health and Medical Officer CIO Chief Information Officer CMMI® Capability Maturity Model® Integration CMMI®-DEV Capability Maturity Model® Integration® (CMMI®) for evelopment CMU Carnegie Mellon University CO Contracting Officer COR Contracting Officer Representative COTS Commercial-Off-the-Shelf CSCI Computer Software Configuration Item CSMA Chief, Safety and Mission Assurance EDL Entry, Descent, and Landing ETA Engineering Technical Authority

- [ ] wrong · n003 · 8607aec804e659e4 · *6.2 Software Engineering Product Content* (p45)
  > MC/DC Modified Condition/Decision Coverage MDAA Mission Directorate Associate Administrator MOTS Modified Off-the-Shelf NASA National Aeronautics and Space Administration NPD NASA Policy Directive NPR 7150.2D -- AppendixB This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7150.2D -- AppendixB Page 53 of 89 NPR NASA Procedural Requirements NTR New Technology Report OCE Office of the Chief Engineer OCHMO Office of Chief Health and Medical Officer OCIO Office of Chief Information Officer OP 

- [ ] wrong · n003 · 8dd692e4766405cb · *Appendix A: Acronyms* (p183)
  > NPD NASA Policy Directive NPR NASA Procedural Requirements NRC (U.S.) Nuclear Regulatory Commission NSTS National Space Transportation System OCE (NASA) Office of the Chief Engineer OCIO (NASA) Office of the Chief Information Officer OCL Object Constraint Language OMB (U.S.) Office of Management and Budget ORR Operational Readiness Review OTS Off-the-Shelf OWL Web Ontology Language PBS Product Breakdown Structure PCA Physical Configuration Audit or Program Commitment Agreement PD/NSC (U.S.) Presidential Directive/National Security Council PDR Preliminary Design Review PFAR Post-Flight Assessme

- [ ] wrong · n003 · ce599a7677e2733a · *Appendix A: Acronyms* (p183)
  > AADL Architecture Analysis and Design Language AD2 Advancement Degree of Difficulty Assessment AIAA American Institute of Aeronautics and Astronautics AO Announcement of Opportunity AS9100 Aerospace Quality Management Standard ASME American Society of Mechanical Engineers ASQ American Society for Quality CAIB Columbia Accident Investigation Board CCB Configuration Control Board CDR Critical Design Review CE Concurrent Engineering or Chief Engineer CEQ Council on Environmental Quality CERR Critical Event Readiness Review CHSIP Commercial Human Systems Integration Processes CI Configuration Item

- [ ] wrong · n003 · bacc1a05ce185156 · *Appendix A: Acronyms* (p183)
  > SRS Software Requirements Specification STI Scientific and Technical Information STS Space Transportation System SysML System Modeling Language T&E Test and Evaluation TA Technical Authority TBD To Be Determined TBR To Be Resolved ToR Terms of Reference TPM Technical Performance Measure TRL Technology Readiness Level TRR Test Readiness Review TVC Thrust Vector Controller UFE Unallocated Future Expenses UML Unified Modeling Language V&V Verification and Validation WBS Work Breakdown Structure WYE Work Year Equivalent XMI XML Metadata Interchange XML Extensible Markup Language

- [ ] wrong · n003 · ef98d73c529d092a · *Appendix A: Acronyms* (p183)
  > DOD (U.S.) Department of Defense DODAF DOD Architecture Framework DR Decommissioning Review DRM Design Reference Mission DRR Disposal Readiness Review EDL Entry, Descent, and Landing EEE Electrical, Electronic, and Electromechanical EFFBD Enhanced Functional Flow Block Diagram EIA Electronic Industries Alliance EMC Electromagnetic Compatibility EMI Electromagnetic Interference EO (U.S.) Executive Order EOM End of Mission EVM Earned Value Management FA Formulation Agreement FAD Formulation Authorization Document FAR Federal Acquisition Regulation FCA Functional Configuration Audit FFBD Function

## n058 · paraphrase · dev

**Query:** How should a project manager handle software upkeep and record keeping during maintenance?

- [ ] wrong · n058 · 4c4c184d26813ea3 · *4.6 Software Operations,* (p73)
  > 4.6.5 195 The project manager shall maintain the software using standards and processes per the applicable software classification throughout the maintenance phase. Center X X X X CIO X 4.6.6 196 The project manager shall identify the records and software tools to be archived, the location of the archive, and procedures for access to the products for software retirement or disposal. Center X X X X CIO X

- [ ] wrong · n058 · 5ec701d54697e1db · *4.6 Software Operations, Maintenance, and Retirement* (p37)
  > have been implemented, and that all defects designated for resolution prior to delivery have been resolved. [SWE-194] NPR 7150.2D -- Chapter4 This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check 4.6.5 The project manager shall maintain the software using standards and processes per the applicable software classification throughout the maintenance phase. [SWE-195] 4.6.6 The project manager shall identify the records and software tools to be archived, the location of the archive, and procedures f

- [ ] wrong · n058 · 1c418d7ca24f66de · *4.6 Software Operations,* (p73)
  > Maintenance, and Retirement 4.6.2 075 The project manager shall plan and implement software operations, maintenance, and retirement activities. Center X X X X CIO X 4.6.3 077 The project manager shall complete and deliver the software product to the customer with appropriate records, including as-built records, to support the operations and maintenance phase of the software’s life cycle. Center X X X X CIO X 4.6.4 194 The project manager shall complete, prior to delivery, verification that all software requirements identified for this delivery have been met or dispositioned, that all approved 

- [ ] wrong · n058 · 94c2f8e6231e3a11 · *4.6 Software Operations, Maintenance, and Retirement* (p37)
  > 4.6.1 Planning for operations, maintenance, and retirement are typically considered throughout the software life cycle. Operational concepts and scenarios are derived from customer requirements and validated in the operational or simulated environment. Software maintenance activities sustain the software product after the product is delivered to the customer until retirement. 4.6.2 The project manager shall plan and implement software operations, maintenance, and retirement activities. [SWE-075] 4.6.3 The project manager shall complete and deliver the software product to the customer with appr

## n017 · exact_id · test

**Query:** software product maturity HDBK

- [ ] wrong · n017 · 533f01a93a4baadc · *5.2 Life-Cycle and Technical Review Requirement* (p36)
  > table. For further description of the primary SE work products, refer to Appendix G. For additional guidance on software product maturity for program/project life-cycle reviews, refer to NASA-HDBK-2203. Additional programmatic work products are required by the governing program/project management NPRs, but not listed herein. 5.2.2.4 The expectation for work products identified as "baselined" in Section 5.2.2.2 and Table 5-1 is that they will be at least final drafts going into the designated life-cycle review. Subsequent to the review, the NPR 7123.1D -- Chapter5 This document does not bind th

- [ ] wrong · n017 · 3fa5701a8c5e4688 · *3.9 Software Development Processes and Practices* (p66)
  > 3.9.2 032 The project manager shall acquire, develop, and maintain software from an organization with a non-expired CMMI®-DEV rating as measured by a CMMI® Institute Certified Lead Appraiser as follows: a. For Class A software: CMMI®-DEV Maturity Level 3 Rating or higher for software. b. For Class B software (except Class B software on NASA Class D payloads, as defined in NPR 8705.4): CMMI®-DEV Maturity Level 2 Rating or higher for software. HQ OCE and HQ OSMA X X

- [ ] wrong · n017 · 78899a922c81eb50 · *3.9 Software Development Processes and Practices* (p28)
  > the period they are responsible for the development and maintenance of the software. CMMI® ratings can cover a team, a group, a project, a division, or an entire organization. For Class B software, an exception can be exercised for those cases in which NASA wishes to purchase a product from the "best in class provider," but the best in class provider does not have the required CMMI® rating. For Class B software, instead of a CMMI® rating by a development organization, the project will conduct an evaluation, performed by a qualified evaluator selected by the Center ETA, against the CMMI®-DEV Ma

- [ ] wrong · n017 · 4c0313689b2bcc01 · *3.9 Software Development Processes and Practices* (p28)
  > e. Identify potential risk areas within a given organization’s software development processes and practices. 3.9.2 The project manager shall acquire, develop, and maintain software from an organization with a non-expired CMMI®-DEV rating as measured by a CMMI® Institute Certified Lead Appraiser as follows: [SWE-032] a. For Class A software: CMMI®-DEV Maturity Level 3 Rating or higher for software. b. For Class B software (except Class B software on NASA Class D payloads, as defined in NPR 8705.4): CMMI®-DEV Maturity Level 2 Rating or higher for software. Note: Organizations need to complete an

- [ ] wrong · n017 · e05b38b5af726829 · *Appendix K: Technical Plans* (p245)
  > The following table represents a typical expectation of maturity of some of the key technical plans developed during the SE processes. This example is for a space flight project. Requirements for work product maturity can be found in the governing PM document (i.e., NPR 7120.5) for the associated type of project. TABLE K-1 Example of Expected Maturity of Key Technical Plans Plan Pre- Phase A Phase A Phase B Phase C Phase D Phase E Phase F Ref. Page MCR SRR SDR/ MDR PDR CDR SIR ORR MRR/ FRR DR DRR Systems Engineering Management Plan P B U U U U U U U U Risk Management Plan A B U U U Integrated 

## n064 · paraphrase · test

**Query:** What key elements are included in the program plan appendix for each project?

- [ ] wrong · n064 · 58d97e03cc5346e3 · *3 Program Life Cycles, Oversight, and Activities by Phase > 3.3 Program Formulation > 3.3.3 Program Management, Planning, and Control Activities* (p75)
  > controlled program requirements document prepared by the program team 5 Bolding indicates required products. 6 NASA-STD-8709.20, Management of Safety and Mission Assurance Technical Authority (SMA TA) Requirements provides further information on selecting SMA standards. For each known project, the program team develops an appendix to the Program Plan or separate document that includes a top-level description of the project, including the mission’s science or exploration objectives; the project’s category, governing PMC, and risk classification; and the project’s mission, performance, and safet

- [ ] wrong · n064 · 31440758116cf283 · *6.0 APPENDICES* (p116)
  > Plan. The Project Plan is updated and approved during the project life cycle in response to changes in program requirements on the project or the baseline commitments. H.1.2 In this Project Plan template, all subordinate plans, collectively called control plans, are required unless they are not applicable or are marked as “Best Practice” in the applicable table in Appendix I (i.e., I-Table). (The expectation is that products marked as “Best Practice” will be developed per the I-Table as part of normal project management activities.) They are based on requirements in NASA Policy Directives (NPD

- [ ] wrong · n064 · 1c4486dde3b73bc9 · *6.0 APPENDICES* (p116)
  > appropriate part of the Project Plan. Considerations for determining if a control plan should be a stand-alone document include a requirement that the control plan be stand-alone in the NPR that requires the control plan; differences between when the control plan is baselined and when the Project Plan is baselined; how frequently the control plan will be updated since updates to the Project Plan require signatures; and how long the control plan is. When the control plan is a stand-alone document, the Project Plan contains a reference to the stand-alone document. H.1.3 Each section of the Proje

## n018 · exact_id · dev

**Query:** IEEE 1028 software peer reviews

- [ ] wrong · n018 · 0e2829887ab722eb · *6.2 Software Engineering Product Content* (p45)
  > (Source: IEEE 1028). Refer to NASA-STD-8739.9 for guidelines for software peer reviews or inspections. NPR 7150.2D -- AppendixA This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7150.2D -- AppendixA Page 50 of 89 Software Reuse. A software product developed for one use but having other uses or one developed specifically to be usable on multiple projects or in multiple roles on one project. Examples include, but are not limited to, COTS products, acquirer-furnished software products, soft

## n032 · exact_id · dev

**Query:** TBD items disposition plan

- [ ] wrong · n032 · 8f0ad322922323d9 · *6.2 Technical Team Responsibilities* (p42)
  > The following primary product is ready for review: 8. **Updated decommissioning plan. a. Other DR technical products have been made available to the cognizant participants prior to the review: 9. *Updated cost.a. Updated schedule.b. *Updated disposal plan. c. identified and are available to successfully complete all decommissioning activities. All required support systems for decommissioning are available. 5. All personnel have been properly trained for the nominal and contingency decommissioning procedures. 6. Safety, health, and environmental hazards have been identified, and controls have b

- [ ] wrong · n032 · c79ac26d554fc1e6 · *6.2 Technical Team Responsibilities* (p42)
  > documented with technology assets, heritage products, and gaps identified. f. *Updated cost and schedule data with ranges and a basis of the estimates. g. *Preliminary Integrated Logistics Support Plan (ILSP). h. *Updated Human Systems Integration approach . (For additional guidance on HSI entrance criteria refer to NASA/SP-20210010952, NASA Human Systems Integration (HSI) Handbook). i. *Updated Human Rating Certification Package. j. demonstrated compliance with applicable NASA and implementing Center requirements, standards, processes, and procedures. TBD and TBR items are clearly identified 

- [ ] wrong · n032 · 154385e188d99690 · *6.2 Technical Team Responsibilities* (p42)
  > Evidence is provided that the program is compliant with NASA and implementing Center requirements, standards, processes, and procedures. 7. To-be-determined (TBD) and to-be-resolved (TBR) items are clearly identified with acceptable plans and schedules for their disposition. 8. The responsible Center spectrum manager at the responsible Center was notified of preliminary requirements. 9. Proposed tailoring is appropriate and consistent with applicable Agency and Center guidance. 10. Lessons Learned from other projects and programs have been identified and addressed. 11. NPR 7123.1D -- AppendixG

- [ ] wrong · n032 · 7f9635327984b9ca · *6.2 Technical Team Responsibilities* (p42)
  > Major risks have been identified and technically assessed, and viable mitigation strategies have been defined. 6. The program/project has demonstrated compliance with applicable NASA and implementing Center requirements, standards, processes, and procedures. 7. TBD and TBR items are clearly identified with acceptable plans and schedule for their disposition. 8. Software components meet the success criteria defined in 9. NPR 7123.1D -- AppendixG This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Che

## n098 · distractor · test

**Query:** Who must approve software testing conducted outside the development team?

- [ ] wrong · n098 · c62c1d980b396fec · *4.5 Software Testing* (p35)
  > testing planned, conducted, witnessed, and approved by an independent organization outside of the development team. 4.5.4 The project manager shall place software items under configuration management prior to testing. [SWE-187] NPR 7150.2D -- Chapter4 This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check Note: This includes the software components being tested and the software components being used to test the software, including components such as support software, models, simulations, ground s

## n042 · paraphrase · test

**Query:** What is required before launching a spacecraft regarding frequency use approval?

- [ ] wrong · n042 · 7c59da44fc7694b7 · *6.2 Technical Team Responsibilities* (p42)
  > certification of spectrum support at Stage 4. At this point, the intended frequency band will have been determined and certification at Stage 3 will be required for testing of proposed operational hardware and potential equipment configurations. (Refer to NPR 2570.1.) Spectrum Certification Stage 4, Operational: Development has been essentially completed, and final operating constraints or restrictions required to assure compatibility need to be identified. Certifying spectrum support for major telecommunication systems or subsystems at Stage 4 is a prerequisite for NTIA authorization to radia

- [ ] wrong · n042 · 1ead5664e30a186e · *6.2 Technical Team Responsibilities* (p42)
  > incorporated into a contract. This document is uncontrolled when printed. Check NPR 7123.1D -- AppendixG Page 97 of 138 certification signed by NTIA. ***All requisite spectrum (radio frequency) authorizations are in place. 9. Updated list of all single point failures and their effects. 10. Supporting organizations are ready to support flight/mission operations. 11. Software components meet the success criteria defined in NASA-HDBK-2203. 12. Responsible Center spectrum manager(s) concur that all necessary spectrum certification(s) and authorization(s) have been obtained. 13. *Product is require

- [ ] wrong · n042 · 0f694343b7bbfdb7 · *5.2 Life-Cycle and Technical Review Requirement* (p36)
  > 5.2.2.5 Terms for maturity levels of technical work products identified in this section are addressed in detail in Appendix F. 5.2.2.6 The technical team ensures that each program or project hosting equipment, experiments, or payloads with radio frequency (RF) requirements include success criteria in all life-cycle and technical reviews to receive approval from the responsible Center spectrum manager that program or project spectrum goals and progress are being achieved and satisfy all spectrum regulatory requirements. Spectrum certification requirements are provided in NPD 2570.5 and NPR 2570

## n038 · exact_id · dev

**Query:** NASA HDBK software defect management

- [ ] wrong · n038 · 7d0f1703ea3207ab · *5.5 Software Non-conformance or Defect Management* (p77)
  > gg. NASA-HDBK-4008, Programmable Logic Devices (PLD) Handbook, https://standards.nasa.gov/. hh. NASA-HDBK-7009, NASA Handbook for Models and Simulations: An Implementation Guide for NASA-STD-7009, https://standards.nasa.gov/. ii. NFS 1813.301-79, Supporting Federal Policies, Regulations, and NASA Procedural Requirements. jj. NFS 1852.237-72, Access to Sensitive Information. kk. NFS 1852.237-73 Release of Sensitive Information. ll. NIST 800-146, Cloud Computing Synopsis and Recommendations. mm. NIST 800-37, Risk Management Framework. nn. NIST 800-53, Security and Privacy Controls for Federal In

- [ ] wrong · n038 · 6d89f08bbd67764d · *5.5 Software Non-conformance or Defect Management* (p77)
  > Class F: General Purpose Computing, Business, and IT Software NPR 7150.2D -- AppendixD This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7150.2D -- AppendixD Page 85 of 89 a. Definition: General purpose computing Business and IT software used in support of the Agency, multiple Centers, multiple programs/projects, single Centers/projects, or locally deployed General Purpose Infrastructure To-Be Component of the NASA Enterprise Architecture. These software applications are generally used t

- [ ] wrong · n038 · 3b28940d73312416 · *5.5 Software Non-conformance or Defect Management* (p77)
  > 1. Space Systems include the following types of software: (a) Flight or ground software necessary for the science return from a single (non-primary) instrument; (b) Flight or ground software used to analyze or process mission data; (c) Other software for which a defect could adversely impact the attainment of some secondary mission objectives or cause operational problems; (d) Software used for the testing of space assets; (e) Software used to verify system requirements of space assets by analysis; or (f) Software for space flight operations not covered by Class A or B software. 2. Aeronautic 

- [ ] wrong · n038 · 9787d08e7831aa17 · *5.5 Software Non-conformance or Defect Management* (p77)
  > Class E: Design Concept, Research, Technology, and General Purpose Software a. Definitions: NPR 7150.2D -- AppendixD This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7150.2D -- AppendixD Page 84 of 89 1. Software developed to explore a design concept or hypothesis but not used to make decisions for an operational Class A, B, or C system or a to-be-built Class A, B, or C system. 2. Software used to perform minor analyses of science or experimental data. 3. A defect in Class E software ma

- [ ] wrong · n038 · 5e92c75599fd9ca8 · *5.5 Software Non-conformance or Defect Management* (p77)
  > 1. Flight systems (i.e., software that meets the flight portions of Class A, B, C, or D Software Classifications); 2. Software developed by or for NASA to directly support an operational system (e.g., human-rated space system, robotics spacecraft, space instrument, airborne vehicle, major engineering/research facility, mission support facility, and primary/major science data collection storage and distribution systems); 3. Software developed by or for NASA to be flight qualified to support an operational system; 4. Software that directly affects primary or secondary mission objectives; 5. Soft

- [ ] wrong · n038 · f855abf0da5051e8 · *5.5 Software Non-conformance or Defect Management* (p77)
  > NPR 8705.4 to examples of Class C software. 2. Aeronautics Vehicles: Guidance, navigation, and control; flight management systems; autopilot; propulsion systems; power systems; emergency systems (e.g., fire suppression systems, emergency egress systems, emergency oxygen supply systems, traffic/ground collision avoidance system); cabin pressure and temperature control; in-flight telescope control software; aviation data integration systems; automated flight planning systems and primary/major science data collection storage and distribution systems (e.g., Distributed Active Archive Centers); sou

- [ ] wrong · n038 · ce842d8dcf8774ec · *5.5 Software Non-conformance or Defect Management* (p77)
  > incorporated into a contract. This document is uncontrolled when printed. Check NPR 7150.2D -- AppendixD Page 80 of 89 systems are limited to software that is: (a) Required to operate the vehicle or space asset (e.g., orbiter, lander, probe, flyby spacecraft, rover, launch vehicle, or primary instrument) such as commanding of the vehicle or asset; (b) Required to achieve the primary mission objectives; or (c) Required to directly prepare resources (data, fuel, power) that are consumed by the above functions. 2. Aeronautic Vehicles include large scale2 aeronautic software systems unique to NASA

- [ ] wrong · n038 · 9f3b4a5e304f79f4 · *5.5 Software Non-conformance or Defect Management* (p77)
  > (d) Ground software tools that support mission planning or formulation; (e) Ground software that operates a research, development, test, or evaluation laboratory (i.e., not a major engineering/research facility); or (f) Ground software that provides decision support for non-mission critical situations. NPR 7150.2D -- AppendixD This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7150.2D -- AppendixD Page 83 of 89 2. Airborne Vehicle Systems include: (a) Software whose anomalous behavior wou

- [ ] wrong · n038 · 5d2f1da5cd5c64ca · *5.5 Software Non-conformance or Defect Management* (p77)
  > operated by or for NASA needed to perform a primary mission objective of human space flight and directly interact with human space flight systems. Limited to software required to perform “vehicle, crew, or primary mission function,” as defined by software that is: (a) Required to operate the vehicle or space asset (e.g., spacesuit, rover, or outpost), including commanding of the vehicle or asset. (b) Required to sustain a safe, habitable1 environment for the crew. (c) Required to achieve the primary mission objectives. (d) Required to directly prepare resources (e.g., data, fuel, power) that a

- [ ] wrong · n038 · c4a04e8d2ceaab5f · *5.5 Software Non-conformance or Defect Management* (p77)
  > and test environments; software used to verify system-level requirements associated with Class A, B, or C software by analysis (e.g., guidance, navigation, and control system performance verification by NPR 7150.2D -- AppendixD This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7150.2D -- AppendixD Page 82 of 89 analysis); simulators used for mission training; software employed by network operations and control (which is redundant with systems used at tracking complexes); command and cont

## n013 · exact_id · test

**Query:** NPR 7150.2D software engineering products

- [ ] wrong · n013 · 8b73c15c46ddff7b · *6.1 Software Engineering Products* (p44)
  > e. Software Change Reports. f. Software Test Plans. g. Software Test Procedures. h. Software Test Reports. i. Software Version Description Reports. j. Software Maintenance Plan. k. Software Assurance Plan(s). l. Software Safety Plan. m. Software Requirements Specification. n. Software Data Dictionary. o. Software and Interface Design Description (Architectural Design). p. Software Design Description. q. Software User’s Manual. r. Records of Continuous Risk Management for Software. s. Software Measurement Analysis Results. NPR 7150.2D -- Chapter6 This document does not bind the public, except a

## n050 · paraphrase · test

**Query:** What methods are used to confirm the quality of different system components?

- [ ] wrong · n050 · ed58ed88da12e28d · *Appendix I: Verification and Validation Plan Outline* (p226)
  > ification/validation) testing/analysis that will be per - formed on the various assemblies that will be tested together and the pedigree of the units that will be used. This may include system-level testing of configurations using engineering units, breadboard, simulators, or other forms or combination of forms. 7.1.2 Verification Activities This section describes the verification activities that will be performed on the various assemblies. 7.1.2.1 Verification by T esting This section describes all verification testing that will be performed on the various assemblies. The section may be broke

- [ ] wrong · n050 · 8abc847da721f6aa · *Appendix I: Verification and Validation Plan Outline* (p226)
  > subsystem, or system level, and the pedigree (flight unit, qualification unit, engineering unit, etc.) of the units these tests will be performed on. 4.2.4.2 Other T esting This section describes any other testing that will be used as part of the verification activities that are not part of the qualification testing. It includes any testing of requirements within the normal operating range of the end item. It may include some engineering tests that will form the foundation or provide dry runs for the official verification testing. 4.3 Validation Methods This section defines and describes the m

- [ ] wrong · n050 · 5f3700de73ce66af · *5.0 Product Realization > 5.3 Product Verification > 5.3.1 Process Description* (p99)
  > design features or specific manufacturer identification. For example, if there is a requirement that the safety arming pin has a red flag with the words “Remove Before Flight” stenciled on the flag in black letters, a visual inspection of the arming pin flag can be used to determine if this requirement was met. Inspection can include inspection of drawings, documents, or other records. Test: The use of an end product to obtain detailed data needed to verify performance or provide sufficient information to verify performance through further analysis. Testing can be conducted on final end produc

- [ ] wrong · n050 · b1bcea9fe4ba5657 · *Appendix I: Verification and Validation Plan Outline* (p226)
  > 4.2.2 Inspection Defines what this verification method means (See Appendix B of this handbook) and how it will be applied to this system. 4.2.3 Demonstration Defines what this verification method means (See Appendix B of this handbook) and how it will be applied to this system. 4.2.4 Test Defines what this verification method means (See Appendix B of this handbook) and how it will be applied to this system. This category may need to be broken down into further categories. Appendix I: Verification and Validation Plan Outline 4.2.4.1 Qualification T esting This section describes the test philoso

- [ ] wrong · n050 · 16add132b34321d8 · *5.0 Product Realization > 5.3 Product Verification > 5.3.1 Process Description* (p99)
  > product requirement. The verification lead should ensure that the procedures were followed and per - formed as planned, the verification-enabling prod - ucts and instrumentation were calibrated correctly, and the data were collected and recorded for required verification measures. A verification program may include verifications at several layers in the product hierarchy. Some verifica- tions need to be performed at the lowest component level if the ability to verify a requirement at a higher assembly is not possible. Likewise, there may be veri- fications at assemblies, sub-systems and system

- [ ] wrong · n050 · 01eb982dbb3a6bff · *5.0 Product Realization > 5.3 Product Verification > 5.3.1 Process Description* (p99)
  > to perform the Product Verification Process. This may include test fixtures and support equipment. Additional work products such as the ConOps, mis- sion needs and goals, interface control drawings, test- ing standards and policies, and Agency standards and policies may also be needed to put verification activ - ities into context. 5.0 Product Realization DIFFERENCES BETWEEN VERIFICATION, QUALIFICATION, ACCEPTANCE AND CERTIFICATION Verification: Verification is a formal process, using the method of test, analysis, inspection or demonstration, to confirm that a system and its associated hardwar

## n026 · exact_id · dev

**Query:** Baseline requirements at SDR

- [ ] wrong · n026 · eaafdda305edae33 · *3.7 Use of the Metric System* (p51)
  > 3. Risk Management Plan [Baseline at SDR] [Required NPR 8000.4] OSMA Yes A Table I-3 4. Acquisition Strategy [Baseline at SDR] [Required per NPD 1000.5] NASA AA No A Table I-3 6. Systems Engineering Management Plan [Baseline at SDR] [Required per NPR 7123.1] OCE Yes A Table I-3 7. Verification and Validation Plan [Baseline at PDR] [Required per NPR 7120.5, additional information in NPR 7123.1] OCE Yes A Table I-3 8. System Security Plan [Baseline at CDR] [Required per NPR 2810.1] OCIO No A Table I-3 9. Review Plan [Baseline at SRR] [Required per NPR 7120.5] NASA AA No A Table I-3 10. Mission O

- [ ] wrong · n026 · d7c2324df7e2ffcc · *3.7 Use of the Metric System* (p51)
  > 9. Documentation of performance against plan/baseline, including status/closure of formal actions from previous KDP [Required per NPR 7120.5] NASA AA No A Table I-1 10. Industrial Base and Supply Chain Risk Management (SCRM) Strategy and Status [Baseline at SDR] [Required per NPR 8735.2] OSMA No A Program Plan Control Plans Table I-1 1. Technical, Schedule, and Cost Control Plan [Baseline at SDR] [Required per NPR 7120.5] NASA AA No A Table I-1 2. Safety and Mission Assurance Plan [Baseline at SDR] [Required per NPRs 8705.2 and 8705.4] OSMA Yes A Table I-1 3. Risk Management Plan [Baseline at 

- [ ] wrong · n026 · d3b2f94fd66decbb · *3.7 Use of the Metric System* (p51)
  > 9. NEPA Compliance Plan [Baseline at SDR] [Required per NPR 8580.1] OSI-EMD No A Table I-1 10. Configuration Management Plan [Baseline at SDR] [Required per NPR 7120.5; additional information in NPR 7123.1 and SAE/EIA 649] OCE Yes A Table I-1 11. Security Plan [Baseline at SDR] [Required per NPR 1040.1 and NPR 1600.1] OPS No A Table I-1 12. Technology Transfer (formerly Export) Control Plan [Baseline at SDR] [Required per NPR 2190.1] OIIR No A Table I-1 15. Quality Assurance Surveillance Plan [Baseline at SDR] [Required per NPR 8735.2 and NASA FAR Supplement part 1837.604] OSMA Yes A Table I-2

- [ ] wrong · n026 · afaa3d2f64ff5e33 · *3.7 Use of the Metric System* (p51)
  > requirements and constraints [Baseline at SDR] [Required per NPR 7123.1] OCE Yes A A Table I-1 3.c. Documentation of driving ground rules and assumptions on the program [Baseline at SDR] [Required per NPR 7120.5] NASA AA No A A Table I-1 4. Interagency and international agreements [Baseline at SDR] NASA AA No A A Table I-1 5. ASM Decision Memorandum [additional information in NPD 1000.5] NASA AA No A A NPR 7120.5F -- AppendixC This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7120.5F -- 

- [ ] wrong · n026 · ecf123e080c9a4b1 · *3.7 Use of the Metric System* (p51)
  > [Baseline at SRR] [Required per NPR 7123.1] OCE Yes A A Table I-6 4. Documentation of driving mission, technical, and programmatic ground rules and assumptions [Baseline at SDR/MDR] [Required per NPR 7120.5] NASA AA No A A Table I-6 5. Partnerships and inter-agency and international agreements [Baseline U.S. partnerships and agreements at SDR/MDR; Baseline international agreements at PDR] NASA AA No A A Table I-6 6. ASM Decision Memorandum [additional information in NPD 1000.5] NASA AA No A A Table I-6 7. Mishap Preparedness and Contingency Plan [Baseline at SMSR] [Required per NPR 8621.1] OSM

- [ ] wrong · n026 · 0751a4458ff65ee1 · *3.7 Use of the Metric System* (p51)
  > [Baseline at SRR] [Required per NPR 7123.1] OCE Yes A A Table I-2 3.b. Traceability of program-level requirements on projects to the Agency strategic goals and Mission Directorate requirements and constraints [Baseline at SDR] [Required per NPR 7123.1] OCE Yes A A Table I-2 3.c. Documentation of driving ground rules and assumptions on the program [Baseline at SDR] [Required per NPR 7120.5] NASA AA No A A Table I-2 4. Interagency and international agreements [Baseline at SDR] NASA AA No A A Table I-2 5. ASM Decision Memorandum [additional information in NPD 1000.5] NASA AA No A A Table I-2 6. R

- [ ] wrong · n026 · 3df5c6097c0002e1 · *6.0 Crosscutting Technical Management > 6.5 Configuration Management > 6.5.1 Process Description* (p154)
  > Baselines are established by agreeing to (and docu - menting) the stated definition of a CI’s attributes. The approved “current” baseline defines the basis of the subsequent change. The system specification is typically finalized following the SRR. The functional baseline is established at the SDR and will usually transfer to NASA’s control at that time for contract - ing efforts. For in-house efforts, the baseline is set/ controlled by the NASA program/project. The four baselines (see FIGURE 6.5-3 ) normally con - trolled by the program, project, or Center are the following: • Functional Base

- [ ] wrong · n026 · be8bd786937aa39f · *6.2 Technical Team Responsibilities* (p42)
  > incorporated into a contract. This document is uncontrolled when printed. Check NPR 7123.1D -- AppendixH Page 123 of 138 indicators. in graphical form but could also be tabular or other form appropriate for the project. At SDR this will be the initial set of trends that have been captured since SRR. Since final hardware has not been produced at this point, the trends will be on the estimated parameters. Req ID NPRSection Requirement Statement Rationale Comply? Justification SE-44 5.2.2.2.c (5) The technical team shall provide the following minimum products at the associated life-cycle review a

- [ ] wrong · n026 · 45154a1f0e122dca · *6.2 Technical Team Responsibilities* (p42)
  > key performance NPR 7123.1D -- AppendixH This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7123.1D -- AppendixH Page 122 of 138 key performance parameters, leading or lagging indicators, or other measures that are important to periodically measure and track. SE-41 5.2.2.2.c (2) The technical team shall provide the following minimum products at the associated life-cycle review at the indicated maturity level: MDR/SDR: Baselined architecture definition. One of the key products of an SDR is

- [ ] wrong · n026 · 2686705a185ffe0e · *3.7 Use of the Metric System* (p51)
  > SDR/MDR] [additional information in NPR 8715.26] OSMA No A Table I-5 24. Range Safety Risk Management Process Documentation [Baseline at SIR] [Required per NPR 8715.5] OSMA Yes A Table I-5 26. Quality Assurance Surveillance Plan [Baseline at SDR] [Required per NPR 8735.2 and NASA FAR Supplement part 1837.604] OSMA Yes A Table I-5 27. Orbital Collision Avoidance Plan [Baseline at PDR] [Required per NPR 8079.1] OCE No A Table I-5 28. Human Systems Integration Approach [Baseline at SRR] [additional information in NASA/SP-20210010952 NASA HSI Handbook and NPR 7123.1] OCE-OSMA-OCHMO1 No A Table I-6

- [ ] wrong · n026 · 9abf6195827a8da3 · *6.2 Technical Team Responsibilities* (p42)
  > at the indicated maturity level: MDR/SDR: Baselined allocation of requirements to next lower level. Now that the overarching architecture has been defined, it is important to show how the requirements are allocated to the architecture elements of the next lower level of the product hierarchy. These are captured in a document or a database/ model. After all comments from the SDR are dispositioned, the allocation is updated with the approved comments and then baselined. SE-43 5.2.2.2.c (4) The technical team shall provide the following minimum products at the associated life-cycle review at the 

## n037 · exact_id · test

**Query:** TRL definition and success criteria

- [ ] wrong · n037 · 082581f256a87ea3 · *6.2 Technical Team Responsibilities* (p42)
  > TRL Definition HardwareDescription SoftwareDescription Success criteria Basic principles observed and reported. Scientific knowledge generated underpinning hardware technology concepts/applications. Scientific knowledge generated underpinning basic properties of software architecture and mathematical formulation. Peer reviewed documentation of research underlying the proposed concept/application. Examples: Initial Paper published providing representative examples of phenomenon as well as supporting equations for a concept. a. Conference presentations on concepts and basic observations presente

- [ ] wrong · n037 · 948301b3000f873a · *6.2 Technical Team Responsibilities* (p42)
  > TRL Definition HardwareDescription SoftwareDescription Success criteria System/sub-system model or prototype demonstration in a relevant environment. A high-fidelity prototype of the system/subsystems that adequately addresses all critical scaling issues is built and tested in a relevant environment to demonstrate performance under critical environmental conditions. Prototype implementations of the software demonstrated on full-scale, realistic problems. Partially integrated with existing hardware/software systems. Limited documentation available. Engineering feasibility fully demonstrated. Do

- [ ] wrong · n037 · 8a52f7e0d4034a67 · *6.2 Technical Team Responsibilities* (p42)
  > completed at the earliest possible stage in development. Some components may require life testing on or after TRL 5. Examples: The level is reached when the final product is qualified for the operational environment through test and analysis. Examples are when Cassini and Galileo were qualified, but not yet flown. a. Interim Cryo Propulsion Stage (ICPS): A Delta Cryogenic Second Stage modified to meet Space Launch System requirements for Exploration Mission-1 (EM-1). Qualified and accepted by NASA for flight on EM-1. b. TRL Definition HardwareDescription SoftwareDescription Success criteria Ac

- [ ] wrong · n037 · 2a6351e25bfeba08 · *6.2 Technical Team Responsibilities* (p42)
  > TRL Definition HardwareDescription SoftwareDescription Success criteria Component and/or breadboard validation in a laboratory environment. A low fidelity system/component breadboard is built and operated to demonstrate basic functionality in a laboratory environment. Key, functionality critical software components are integrated and functionally validated to establish interoperability and begin architecture development. Relevant environments defined and performance in the environment predicted. Documented test performance demonstrating agreement with analytical predictions. Documented definit

- [ ] wrong · n037 · efe45294387a40d2 · *6.2 Technical Team Responsibilities* (p42)
  > properties of algorithms, representations, and concepts defined. Basic principles coded. Experiments performed with synthetic data. Documented description of the application/concept that addresses feasibility and benefit. Example: Carbon nanotube composites were created for lightweight, high-strength structural materials for space structures. TRL Definition HardwareDescription SoftwareDescription Success criteria NPR 7123.1D -- AppendixE This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 

- [ ] wrong · n037 · 846d4da51c528106 · *6.2 Technical Team Responsibilities* (p42)
  > In-space demonstration missions for technology (e.g., autonomous robotics and deep space atomic clock). Successful flight demonstration could result in use of the technology in a future operational mission c. Robotic External Leak Locator (RELL): Originally flown as a technology demonstrator, the test article was subsequently put to use to help operators locate the likely spot where ammonia was leaking from the International Space Station (ISS) External Active Thermal Control System Loop B. d. TRL Definition HardwareDescription SoftwareDescription Success criteria Actual system completed and "

- [ ] wrong · n037 · 444924108c2940fc · *Appendices > A. Definitions* (p401)
  > 7120.10, Technical Standards for NASA Programs and Projects.) Technology Readiness Level. Provides a scale against which to measure the maturity of a technology. TRLs range from 1, Basic Technology Research, to 9, Systems Test, Launch, and Operations. Typically, a TRL of 6 (i.e., tech- nology demonstrated in a relevant environment) is required for a technology to be integrated into a flight system. (See Systems Engineering Handbook, NASA/SP-2007-6105 Rev 1, p. 296 for more information on TRL levels and technology assessment.) Termination Review. A review initiated by the Decision Authority for

- [ ] wrong · n037 · 59d16e1b0e32ef24 · *Appendix G: Technology Assessment/Insertion* (p216)
  > terms come from mechanical engineering, referring Appendix G: Technology Assessment/Insertion primarily to units that are subjected to different levels of stress under testing, e.g., qualification, protoflight, and flight units. The first step in developing a uni - form TRL assessment (see FIGURE G.4-2 ) is to define the terms used. It is extremely important to develop and use a consistent set of definitions over the course of the program/project. TRL 1 Basic principles observed and reported TRL 2 Technology concept and/or application form ulated __ TRL 3 Analytical and experimental critical f

- [ ] wrong · n037 · 229b73df7a9c19da · *Appendix G: Technology Assessment/Insertion* (p216)
  > a set of levels first described at NASA HQ in the 1980s. The TRL essentially describes the state of a given technology and provides a baseline from which maturity is gauged and advancement defined. (See FIGURE G.4-1 .) Programs are often undertaken without fully under - standing either the maturity of key technologies or what is needed to develop them to the required level. It is impossible to understand the magnitude and scope of a development program without having a clear understanding of the baseline technological maturity of all elements of the system. Establishing the TRL is a vital firs

- [ ] wrong · n037 · 7eb1e0fb567b8451 · *3.7 Use of the Metric System* (p51)
  > technology. TRLs range from 1, Basic Technology Research, to 9, Systems Test, Launch, and Operations. Typically, a TRL of 6 (i.e., technology demonstrated in a relevant environment) is required for a technology to be integrated into a flight system. (See NASA Systems Engineering Handbook NASA/SP-2016-6105 Rev 2 for more information on TRL levels and technology assessment, and SP-20205003605, Technology Readiness Assessment Best Practices Guide.) Termination Review. A special review convened to determine whether to continue or terminate a program or project. Circumstances that could trigger a T

- [ ] wrong · n037 · 1554296ae70ce8e5 · *Appendix G: Technology Assessment/Insertion* (p216)
  > Has analytical and experimental proof-of-concept been demonstrated? Has concept or application been formulated? Have basic principles been observed and reported? RETHINK POSITION REGARDING THIS TECHNOLOGY! NO NO NO NO NO NO NO NO NO NO TRL 9YES TRL 5YES TRL 2YES TRL 1YES TRL 3YES TRL 4YES TRL 5YES TRL 6YES TRL 7YES TRL 8YES FIGURE G.4-2 TM A Thought Process H eritage Systems Note the second box particularly refers to heritage systems. If the architecture and the environment have changed, then the TRL drops to TRL 5—at least initially. Additional testing may need to be done for heritage systems

## n084 · paraphrase · dev

**Query:** How does NASA incorporate risk and budgeting in project cost and schedule planning?

- [ ] wrong · n084 · 0eb228946ade726b · *5 Special Topics > 5.6 Cost and Schedule Analysis Work to Support Decisions > 5.6.1 Cost and Schedule Estimates* (p308)
  > strategic resource planning. This includes the periodic portfolio reviews and resulting direction and the NASA budget process (i.e., Planning, Programming, Budgeting, and Execution (PPBE)). 13 See NASA-HDBK-2203 (http://swehb.nasa.gov) for information on software cost estimating and cost analysis. 5.6 Cost and Schedule Analysis w ork to Support Decisions ⦁ A risk-informed schedule at KDP 0/KDP A/KDP B and a risk-informed cost- or resource-loaded schedule at all other KDPs. (See Section 5.7 for discussion on resource-loaded versus cost-loaded schedules.) ⦁ Decisions and direction documented in 

- [ ] wrong · n084 · 713e046a408d7802 · *5 Special Topics > 5.7 Realistic Cost and Schedule Estimating and the JCL > 5.7.4 JCL Process Flow (Overview)* (p318)
  > “JCL,” as referred to in this special topic, refers to a probabilistic cost- loaded schedule (PCLS).15 The reason the Agency focuses on the PCLS stems from the fact that the method forces the program or project and the review entity to focus on the program’s or project’s plan. This improves program or project planning by systematically integrating cost, schedule, and risk products and processes. It also facilitates transparency with stakeholders on expectations and the probabilities of meeting those expectations. Lastly, it provides a cohesive and holistic picture of the program or project’s a

- [ ] wrong · n084 · 895296ee75204f4d · *Appendices > C. NPR 7120.5E Requirements Rationale* (p427)
  > $250 million. 2.4.4 Mission Directorates shall plan and budget tightly coupled and single-project programs (regardless of life-cycle cost) and projects (with an estimated life-cycle cost greater than $250 million) based on a 70 percent joint cost and schedule confidence level or as approved by the Decision Authority. In response to GAO cost growth concerns, NASA surveyed the best practices in the industry and determined that all projects need to be estimated using probabilistic cost estimating methods and budgets need to reflect a 70 percent probability the project could be completed for that 

- [ ] wrong · n084 · 3f4638c0f8b92410 · *5 Special Topics > 5.7 Realistic Cost and Schedule Estimating and the JCL > 5.7.4 JCL Process Flow (Overview)* (p318)
  > costs and schedule imbedded in the plan, but risk realization from the risk management system has not been incorporated. Traditionally, NASA programs and projects use their risk management system to help popu - late the risk activities ; however, a JCL analysis does not have to be limited by what is currently being managed in the risk management system. For example, there may be a programmatic risk that does not “make it” into the risk management system but is still of concern to the project manager. The JCL analysis allows the project to model the programmatic consequences and expected value 

## n010 · exact_id · dev

**Query:** SEMP technical planning process

- [ ] wrong · n010 · 762962bbc027ace1 · *6.0 Crosscutting Technical Management > 6.1 Technical Planning > 6.1.1 Process Description* (p124)
  > Resource Constraints To Technical Data Management Process From project From Technical Data Management Process To Technical Assessment Process To project To applicable technical processes To applicable technical teams From Technical Assessment and Technical Risk Management Processes Prepare to conduct technical planning k Schedule, organize, and cost the technical work Prepare SEMP and other technical plans Obtain stakeholder commitments to technical plans Issue authorized technical work directives Capture work products from technical planning activities Agreements, Capability Needs, Applicable

- [ ] wrong · n010 · 8f8eb4855cd24f56 · *6.0 Crosscutting Technical Management > 6.1 Technical Planning > 6.1.1 Process Description* (p124)
  > meet product life cycle phase success criteria. A key document capturing and updating the details from the technical planning process is the SEMP. The SEMP is a subordinate document to the proj - ect plan. The project plan defines how the project will be managed to achieve its goals and objectives within defined programmatic constraints. The SEMP defines for all project participants how the project will be technically managed within the constraints established by the project. The SEMP also commu - nicates how the systems engineering management techniques will be applied throughout all phases o

- [ ] wrong · n010 · 8388c935d0a32d98 · *6.0 Crosscutting Technical Management > 6.1 Technical Planning > 6.1.1 Process Description* (p124)
  > and other technical plans that support implemen- tation of the technical effort (to all processes; applicable plans to technical processes); 6.0 Crosscutting Technical Management • Technical work directives: e.g., work packages or task orders with work authorization (to applicable technical teams); and • Technical Planning Process work products: Includes products needed to provide reports, records, and non-deliverable outcomes of process activities (to the Technical Data Management Process). The resulting technical planning strategy constitutes an outline, or rough draft, of the SEMP. This ser

## n036 · exact_id · dev

**Query:** CRM process risk management

- [ ] wrong · n036 · b1fb383e53d045dc · *3.7 Use of the Metric System* (p51)
  > requirements are met. This is done to foster proactive risk management, to better inform decision making through better use of risk information, and then to more effectively manage Implementation risks by focusing the CRM process on the baseline performance requirements emerging from the RIDM process. (See NPR 8000.4, Agency Risk Management Procedural Requirements.) These processes are applied at a level of rigor commensurate with the complexity, cost, and criticality of the program. Risk-Informed Decision Making. A risk-informed decision-making process that uses a diverse set of performance m

- [ ] wrong · n036 · 2ef4a13e4faf2966 · *6.0 Crosscutting Technical Management > 6.4 Technical Risk Management > 6.4.1 Risk Management Process Description* (p151)
  > outlined in NPR 8000.4, Agency Risk Management Procedural Requirements and further developed in NASA/SP-2011-3422, NASA Risk Management Handbook, evolves NASA‘s risk management to entail two complementary processes: Risk-Informed Decision Making (RIDM) and CRM. RIDM is intended to inform direction-setting systems engi - neering (SE) decisions (e.g., design decisions) through better use of risk and uncertainty information in selecting alternatives and establishing baseline perfor- mance requirements (for additional RIDM technical information, guidance, and process description, see NASA/SP-2010-

- [ ] wrong · n036 · 897151ccaf44ced3 · *Appendix B: Glossary* (p186)
  > Risk-Informed Decision-Making (RIDM) and Continuous Risk Management (CRM) in an inte - grated framework. RIDM informs systems engi - neering decisions through better use of risk and uncertainty information in selecting alternatives and establishing baseline requirements. CRM manages risks over the course of the development and the Implementation Phase of the life cycle to ensure that Appendix B: Glossary safety, technical, cost, and schedule requirements are met. This is done to foster proactive risk man - agement, to better inform decision-making through better use of risk information, and th

- [ ] wrong · n036 · 1cfd8f6d61953c76 · *Appendices > A. Definitions* (p401)
  > schedule. (See NPR 8000.4, Agency Risk Management Procedural Require - ments.) Risk Assessment. An evaluation of a risk item that determines: (1) what can go wrong, (2) how likely is it to occur, (3) what the consequences are, (4) 398 APPENDIX A. DEFINITIONS what the uncertainties are that are associated with the likelihood and conse - quences, and (5) what the mitigation plans are. Risk Management. Risk management includes Risk-Informed Decision Making (RIDM) and Continuous Risk Management (CRM) in an integrated framework. RIDM informs systems engineering decisions through better use of risk 

- [ ] wrong · n036 · 375698605a9fbc7d · *3.7 Use of the Metric System* (p51)
  > requirements. The performance shortfalls may be related to any one or more of the following mission execution domains: (1) safety, (2) technical, (3) cost, and (4) schedule. (See NPR 8000.4, Agency Risk Management Procedural Requirements.) Risk Assessment. An evaluation of a risk item that determines: (1) what can go wrong, (2) how likely is it to occur, (3) what the consequences are, (4) what the uncertainties are that are associated with the likelihood and consequences, and (5) what the mitigation plans are. Risk Management. Risk management includes risk-informed decision making (RIDM) and c

- [ ] wrong · n036 · 8cb6c170a5e92b00 · *3.3 Risk Management Plan* (p124)
  > Develop a Risk Management Plan that includes the content required by NPR 8000.4, Agency Risk Management Procedural Requirements. Summarize how the project will implement a risk management process (including risk-informed decision making (RIDM) and continuous risk management (CRM) in accordance with NPR 8000.4, Agency Risk Management Procedural Requirements). Include the initial Significant Risk List and appropriate actions to mitigate each risk. Projects with international or other U.S. Government agency contributions need to plan for, assess, and report on risks due to international or other 

- [ ] wrong · n036 · ab308804b3c7f9d3 · *3.3 Risk Management Plan* (p109)
  > Develop a Risk Management Plan that includes the content required by NPR 8000.4, Agency Risk Management Procedural Requirements. Summarize how the program will implement the NASA risk management process (including risk-informed decision making (RIDM) and continuous risk management (CRM) in accordance with NPR 8000.4, Agency Risk Management Procedural Requirements. Include the initial Significant Risk List and appropriate actions to mitigate each risk. Programs with international or other U.S. Government agency contributions need to plan for, assess, and report on risks due to international or 

- [ ] wrong · n036 · 6de622fcc231f28d · *Appendices > A. Definitions* (p401)
  > better use of risk information, and then to more effectively manage Imple - mentation risks by focusing the CRM process on the baseline performance requirements emerging from the RIDM process. (See NPR 8000.4, Agency Risk Management Procedural Requirements .) These processes are applied at a level of rigor commensurate with the complexity, cost, and criticality of the program. Risk-Informed Decision Making. A risk-informed decision-making process that uses a diverse set of performance measures (some of which are model- based risk metrics) along with other considerations within a deliberative p

## n023 · exact_id · test

**Query:** CIO authority on Class F software

- [ ] wrong · n023 · 3fb4dae1008127c2 · *3.1 Software Life Cycle Planning* (p20)
  > partially relieved in the Requirements Mapping Matrix. The CIO has institutional authority on all Class F software projects. 3.1.14 The project manager shall satisfy the following conditions when a COTS, GOTS, MOTS, OSS, or reused software component is acquired or used: [SWE-027] a. The requirements to be met by the software component are identified. b. The software component includes documentation to fulfill its intended purpose (e.g., usage instructions). c. Proprietary rights, usage rights, ownership, warranty, licensing rights, transfer rights, and conditions of use (e.g., required copyrig

- [ ] wrong · n023 · 2872d58a66078615 · *6.2 Software Engineering Product Content* (p45)
  > has institutional authority on all Class F software projects and has joint responsibility with the ETA on the cybersecurity requirements in Section 3.11 per the direction in the Requirements Mapping Matrix. CIO - The NASA CIO, or the designee Center CIO, has institutional authority on all Class F software projects and has joint responsibility with the ETA on the cybersecurity requirements in section 3.11, per the direction in the Requirements Mapping Matrix. Each requirement marked ‘X’ for the project’s software classification(s) should be addressed in the Requirements Mapping Matrix. All requ

- [ ] wrong · n023 · 16f9f846fbed6214 · *6.2 Software Engineering Product Content* (p45)
  > d. The Authority Level responsible for assessing a project’s requirements mapping matrices and any requested tailoring from requirements in this NPR. The CIO, or the designee, has institutional authority on all Class F software projects and has joint responsibility on the cybersecurity requirements in Section 3.11. e. The applicability of the requirements in this NPR to specific systems and subsystems within the Agency’s investment areas, programs, and projects is determined through the use of the NASA-wide definition of software classes. C.3 Tailoring Guidance X - Indicates an invoked require

- [ ] wrong · n023 · a97b321a92205fb2 · *6.2 Software Engineering Product Content* (p2)
  > d. For existing Class F programs and projects, the software engineering requirements of this NPR apply to their current and future phases as determined by the Center Chief Information Officer (CIO) and approved by the NASA CIO (or delegate). e. This NPR can be applied to other NASA investments at the discretion of the responsible manager or the NASA Associate Administrator. This NPR is not retroactively applicable to software development, maintenance, operations, management, acquisition, and assurance activities started before the effective date of this NPR (i.e., existing systems and subsyste

- [ ] wrong · n023 · 2fb722a850168576 · *3.1 Software Life Cycle Planning* (p20)
  > matrix or multiple requirements mapping matrices against requirements in this NPR, including those delegated to other parties or accomplished by contract vehicles or Space Act Agreements. [SWE-125] Note: A project may have multiple software engineering requirements mapping matrices if needed for multiple software components on a given project. Note: Project relief from an applicable “X” requirement can be granted only by the designated TAs, Engineering, and SMA, or, for security issues, the NASA CIO. The record of their approval of the tailored requirements in a Requirements Mapping Matrix wil

- [ ] wrong · n023 · ace87c700929bca9 · *3.5 Software Classification* (p61)
  > Assessments NPR 7150.2D -- AppendixC This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7150.2D -- AppendixC Page 61 of 89 3.5.1 020 The project manager shall classify each system and subsystem containing software in accordance with the highest applicable software classification definitions for Classes A, B, C, D, E, and F software in Appendix D. Center X X X X X CIO X 3.5.2 176 The project manager shall maintain records of each software classification determination, each software Require

## n021 · exact_id · test

**Query:** NPR control plan requirements

- [ ] wrong · n021 · 015a5a9972aebfc9 · *6.0 APPENDICES* (p132)
  > b. Considerations for determining if a control plan should be a stand-alone document include a requirement that the control plan be stand-alone in the NPR that requires the control plan; differences between when the control plan is baselined and when the Program or Project Plan is baselined; how frequently the control plan will be updated since updates to the Program or Project Plan require signatures; and how long the control plan is. c. When the control plan is a stand-alone document, the Program or Project Plan contains a reference to the stand-alone document.

- [ ] wrong · n021 · b7ca287e06a735ac · *3 Program Life Cycles, Oversight, and Activities by Phase > 3.3 Program Formulation > 3.3.3 Program Management, Planning, and Control Activities* (p75)
  > documented in control plans, which are designed to keep the program activities aligned, on track, and accounted for as the program moves forward. (See Appendix F for a description of control plans required by NPR 7120.5E.) These control plans are described in this and subsequent sections of this handbook, in conjunction with the phase where they are required. Many control plans are incorporated into the central planning document, which is the Program Plan. NPR 7120.5E, Appendix G, identi - fies when a control plan may be included in the Program Plan, and when a control plan is required to be a

- [ ] wrong · n021 · a07f14fe3a9aba12 · *3.16 Technology Transfer (formerly Export) Control Plan* (p114)
  > Describe how the program will implement the export control requirements specified in NPR 2190.1, NASA Export Control Program.

- [ ] wrong · n021 · 36065a9fe0f379fd · *3.19 Technology Transfer (formerly Export) Control Plan* (p130)
  > Describe how the project will implement the export control requirements specified in NPR 2190.1, NASA Export Control Program.

- [ ] wrong · n021 · 608d8bf505c2479e · *15.0 Appendices* (p101)
  > can either be part of the Program Plan or separate stand-alone documents referenced in the appropriate part of the Program Plan. Considerations for determining if a control plan should be a stand-alone document include a requirement that the control plan be stand-alone in the NPR that requires the control plan; differences between when the control plan is baselined and when the Program Plan is baselined; how frequently the control plan will be updated; and how long the control plan is. When the control plan is a stand-alone document, the Program Plan contains a reference to the stand-alone doc

- [ ] wrong · n021 · c1b1bbc5ba879835 · *3.0 NASA Program/Project Life Cycle > 3.4 Project Phase A: Concept and Technology Development* (p33)
  > • Develop and baseline top-level requirements and constraints including internal and external interfaces, integrated logistics and maintenance support, and system software functionality • Allocate system requirements to functions and to next lower level • Validate requirements • Baseline plans > Systems Engineering Management Plan > Human Systems Integration Plan > Control plans such as the Risk Management Plan, Configuration Management Plan, Data Management Plan, Safety and Mission Assurance Plan, and Software Development or Management Plan (See NPR 7150.2) > Other crosscutting and specialty 

- [ ] wrong · n021 · 3f9a83084c2a580c · *1.5 Formats for Non-Control Plan I-Table Products* (p133)
  > NASA AA/R Summary Summary Summary 10. Industrial Base and Supply Chain Risk Management (SCRM) Strategy and Status [Required per NPR 8735.2] OSMA/R Preliminary Baseline Update Program Plan Control Plans 1. Technical, Schedule, and Cost Control Plan [Required per NPR 7120.5] NASA AA/R Preliminary Baseline 2. Safety and Mission Assurance Plan [Required per NPRs 8705.2 and 8705.4] OSMA/R Preliminary Baseline 3. Risk Management Plan [Required per NPR 8000.4] OSMA/R Preliminary Baseline 4. Acquisition Strategy [Required per NPD 1000.5] NASA AA/R Preliminary Baseline 5. Technology Development Plan [a

- [ ] wrong · n021 · 0065c102bba43525 · *1.5 Formats for Non-Control Plan I-Table Products* (p133)
  > 7120.5; additional information in NPR 7123.1 and SAE/EIA 649] OCE/R Baseline Update Update 17. Security Plan [Required per NPR 1040.1 and NPR 1600.1] OPS/R Preliminary Baseline Updateannually 18. Project Protection Plan [Required per NPR 1058.1, additional information in NASA-STD-1006] OCE/R Preliminary Baseline Update Update Update Update Updateannually 19. Technology Transfer (formerly Export) Control Plan [Required per NPR 2190.1] OIIR/R Preliminary Baseline Update NPR 7120.5F -- AppendixI This document does not bind the public, except as authorized by law or as incorporated into a contract

- [ ] wrong · n021 · 0733ff1514896b33 · *1.5 Formats for Non-Control Plan I-Table Products* (p133)
  > SRR SDR PDR CDR SIR ORR MRR/FRR DR 1. Technical, Schedule, and Cost Control Plan [Required per NPR 7120.5] NASA AA/R Preliminary Baseline Update NPR 7120.5F -- AppendixI This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7120.5F -- AppendixI Page 136 of 149 2. Safety and Mission Assurance Plan [Required per NPRs 8705.2 and 8705.4] OSMA/R Preliminary Baseline Update Update Update(SMSR) 3. Risk Management Plan [Required per NPR 8000.4] OSMA/R Preliminary Baseline Update 4. Acquisition Strat

- [ ] wrong · n021 · d7c2324df7e2ffcc · *3.7 Use of the Metric System* (p51)
  > 9. Documentation of performance against plan/baseline, including status/closure of formal actions from previous KDP [Required per NPR 7120.5] NASA AA No A Table I-1 10. Industrial Base and Supply Chain Risk Management (SCRM) Strategy and Status [Baseline at SDR] [Required per NPR 8735.2] OSMA No A Program Plan Control Plans Table I-1 1. Technical, Schedule, and Cost Control Plan [Baseline at SDR] [Required per NPR 7120.5] NASA AA No A Table I-1 2. Safety and Mission Assurance Plan [Baseline at SDR] [Required per NPRs 8705.2 and 8705.4] OSMA Yes A Table I-1 3. Risk Management Plan [Baseline at 

- [ ] wrong · n021 · b1b5d0f76a02b58a · *1.5 Formats for Non-Control Plan I-Table Products* (p133)
  > Appendices G and H for Control Plan Details) Product Owner/Requirement or Best Practice Pre-Phase A Phase A KDP B Phase B KDP C Phase C KDP D Phase D KDP E Phase E KDP F MCR SRR SDR/MDR PDR CDR SIR ORR MRR/ FRR DR 1. Technical, Schedule, and Cost Control Plan [Required per NPR 7120.5] NASA AA/R Approach for managing schedule and cost during Phase A 1 Preliminary Baseline Update 2. Safety and Mission Assurance Plan [Required per NPRs 8705.2 and 8705.4] OSMA/R Baseline Update Update Update Update(SMSR) Update 3. Risk Management Plan [Required per NPR 8000.4] OSMA/R Approach for managing risks du

- [ ] wrong · n021 · 7c26af2921bdce39 · *1.5 Formats for Non-Control Plan I-Table Products* (p133)
  > incorporated into a contract. This document is uncontrolled when printed. Check NPR 7120.5F -- AppendixI Page 134 of 149 8. Review Plan [Required per NPR 7120.5]2 NASA AA/R Baseline Update 9. NEPA Compliance Plan [Required per NPR 8580.1] OSI-EMD/R Baseline 10. Configuration Management Plan [Required per NPR 7120.5; additional information in NPR 7123.1 and SAE/EIA 649] OCE/R Baseline 11. Security Plan [Required per NPR 1040.1 and NPR 1600.1] OPS/R Baseline 12. Technology Transfer (formerly Export) Control Plan [Required per NPR 2190.1] OIIR/R Baseline 13. Communications Plan [additional inform

## n029 · exact_id · dev

**Query:** SRB role in cost estimates

- [ ] wrong · n029 · 679f5196a26dbcff · *5 Special Topics > 5.6 Cost and Schedule Analysis Work to Support Decisions > 5.6.1 Cost and Schedule Estimates* (p308)
  > Cost and schedule estimates have an essential role in program and project management and must have a sound documented basis. All programs and projects develop cost estimates and planned schedules for the work to be performed in the current and following life-cycle phases. As part of devel - oping these estimates, the program or project documents the Basis of Estimate (BoE) in retrievable program or project records. The BoE docu - ments the ground rules, assumptions, and drivers used in cost and schedule estimate development and includes applicable model inputs and outputs, rationale/justificat

- [ ] wrong · n029 · 21febe1c6ddc5043 · *Appendices > A. Definitions* (p401)
  > Baseline Science Requirements. The mission performance requirements necessary to achieve the full science objectives of the mission. (Also see Threshold Science Requirements.) Basis of Estimate. The documentation of the ground rules, assumptions, and drivers used in developing the cost and schedule estimates, including applicable model inputs, rationale or justification for analogies, and details supporting cost and schedule estimates. The BoE is contained in material available to the Standing Review Board (SRB) and management as part of the life-cycle review and Key Decision Point (KDP) proce

## n092 · distractor · dev

**Query:** How do program/project teams assess progress and resolve technical issues early?

- [ ] wrong · n092 · bb4d6e9c957f2221 · *6.2 Technical Team Responsibilities* (p42)
  > requirements satisfaction. This requirement ensures that the program/project and the ETA identifies how they will assess the progress of the program/project's technical efforts, including life-cycle reviews. It ensures that the program/project team, customers, and other key stakeholders know how the effort is progressing and if additional actions are needed to resolve issues prior to becoming too costly. NPR 7123.1D -- AppendixH This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7123.1D -

- [ ] wrong · n092 · 3a508e4b1e1ca748 · *5 Special Topics > 5.10 Independent Standing Review Boards and Life-Cycle Reviews > 5.10.2 Life-Cycle Reviews and Independent Assessment* (p352)
  > Life-cycle reviews are designed to provide the program or project an oppor - tunity to ensure that it has completed the work of that phase and provide an independent assessment of the program or project’s technical and program - matic progress, status, and health against Agency criteria. The independent assessment serves as a basis for the program or project and management to determine if the work has been satisfactorily completed and if the plans for the following life-cycle phases are acceptable. If the program or project’s work has not been satisfactorily completed or its plans are not acce

- [ ] wrong · n092 · facb963964089a79 · *2.1 Roles and Responsibilities Relative to System Engineering* (p14)
  > infrastructure) required for the execution of programs and projects. b. Performing periodic program and project reviews to assess technical and programmatic progress to ensure performance in accordance with their Center's and the Agency requirements, procedures, processes, and other documentation. c. Working with the Mission Directorate and the program and project managers, once assigned, to assemble the program/project team(s) and to provide needed Center resources. d. Providing support and guidance to programs and projects in resolving technical and programmatic issues and risks. 2.1.4.2 The

- [ ] wrong · n092 · 3fc8f9b486e5e2f6 · *5 Special Topics > 5.1 NASA Governance > 5.1.2 Institutional Authority* (p252)
  > ⦁ Supports programs and projects by providing needed Center resources; providing support and guidance to programs and projects in resolving technical and programmatic issues and risks; monitoring the technical and programmatic progress of programs and projects to help identify issues as they emerge; and proactively working with the Mission Direc - torates, programs, projects, and other Institutional Authorities to find constructive solutions to problems. ⦁ Proactively works on cross-Center activities to benefit both the programs and projects and the overall Agency long-term health. As part of 

- [ ] wrong · n092 · ccbc878001543ade · *5 Special Topics > 5.13 NASA Required and Recommended Leading Indicators > 5.13.3 Required Leading Indicators* (p376)
  > ⦁ Total number of RFAs, RIDs, or action items (whichever the program or project uses). ⦁ Number of open RFAs, RIDs, or action items (whichever the program or project uses). ⦁ The planned rate for addressing and resolving or “burndown rate” of these items. Table 5-9 shows an example spreadsheet tracking the number of RFAs for a given life-cycle review. Note that data are gathered monthly, not just at the next life-cycle review. Trending works best if the leading indicator measure - ments are taken regularly. The planned burndown rate of the RFAs is included. While it can be difficult to predict

- [ ] wrong · n092 · 2cffe415d528cc67 · *6.0 Crosscutting Technical Management > 6.7 Technical Assessment > 6.7.1 Process Description* (p167)
  > technical measures that will be tracked and assessed to determine technical progress. An important part of the technical planning is determining what is needed in time, resources, and performance to com - plete a system that meets desired goals and objectives. Project managers need visibility into the progress of those plans in order to exercise proper management control. Typical activities in determining progress against the identified technical measures include sta - tus reporting and assessing the data. Status report - ing will identify where the project stands with regard to a particular t

- [ ] wrong · n092 · c24040c2bfc58e05 · *6.0 Crosscutting Technical Management > 6.7 Technical Assessment > 6.7.1 Process Description* (p167)
  > be carefully scrutinized for early warning signs of potential problems. Should there be indications that existing trends, if allowed to continue, will yield an unfavorable outcome, corrective action should begin as soon as practical. Section 6.7.2.6.1 in the NASA Expanded Guidance for Systems Engineering at https://nen.nasa.gov/web/se/doc-repository pro- vides additional information on status reporting and assessment techniques for costs and schedules (including EVM), technical performance, and sys - tems engineering process metrics. The measures are predominantly assessed during the program a

- [ ] wrong · n092 · 90632d88d2b42fb2 · *5.2 Life-Cycle and Technical Review Requirement* (p36)
  > 5.2.2.7 Technical teams shall monitor technical effort through periodic technical reviews [SE-57]. 5.2.2.8 For each type of program/project, technical efforts are monitored throughout the life cycle to ensure that the technical goals of the program/project are being achieved and that the technical direction of the program/project is appropriate. NPR 7123.1D -- Chapter5 This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7123.1D -- Chapter5 Page 39 of 138 5.2.2.9 A technical review is an ev

- [ ] wrong · n092 · b43a1305fbf2224d · *6.0 Crosscutting Technical Management > 6.7 Technical Assessment > 6.7.1 Process Description* (p167)
  > Expanded Guidance for Systems Engineering at https://nen.nasa.gov/web/se/doc-repository .) • Report these technical measures in a consistent format at all project levels. • Maintain historical data for both trend identifica- tion and cross-project analyses. • Encourage a logical process of rolling up technical measures (e.g., use the WBS or PBS for project progress status). • Support assessments with quantitative risk measures. • Summarize the condition of the project by using color-coded (red, yellow, and green) alert zones for all technical measures. 6.7.1.2.2 Assess T echnical Work Producti

- [ ] wrong · n092 · f354a457ab7f96ab · *6.0 Crosscutting Technical Management > 6.7 Technical Assessment > 6.7.1 Process Description* (p167)
  > These activities together form the feedback loop depicted in FIGURE 6.7-2 . (Re-) Planning Status Reporting Assessing Decision-making Status Not OK Status OK Execute FIGURE 6.7-2 Planning and Status Reporting Feedback Loop This loop takes place on a continual basis throughout the project life cycle. This loop is applicable at each level of the project hierarchy. Planning data, status reporting data, and assessments flow up the hierar - chy with appropriate aggregation at each level; deci - sions cause actions to be taken down the hierarchy. Managers at each level determine (consistent with pol

- [ ] wrong · n092 · 70f03ce70036e7a2 · *3.2 Common Technical Processes Requirements* (p24)
  > process to include activities, requirements, guidelines, and documentation, as tailored and customized for making assessments of the progress of planned technical effort and progress toward requirements satisfaction [SE-22]. 3.2.17.2 The Technical Assessment process is used to help monitor progress of the technical effort and provide status information for support of the system design, product realization, and technical management processes. A key aspect of the technical assessment process is the conduct of life-cycle and technical reviews throughout the system life cycle in accordance with Ch

- [ ] wrong · n092 · 998fa9d78636c0a8 · *5.1 Life Cycle* (p32)
  > products. Additional programmatic work products may also be required by the governing program/project NPR. Programs/projects are expected to tailor the reviews and customize the entrance/success criteria as appropriate to the size/complexity and unique needs of their activities. Approved tailoring is captured in the SEMP or other equivalent program/project documents. 5.1.4 The progress between life-cycle phases is marked by key decision points (KDPs). At each KDP, management examines the maturity of the technical aspects of the program/project. For example, management evaluates the adequacy of

- [ ] wrong · n092 · a8b3fb7a2d395c1f · *6.0 Crosscutting Technical Management > 6.7 Technical Assessment > 6.7.1 Process Description* (p167)
  > From Decision Analysis Process Product and Process Measures Technical Plans From Technical Planning Process From project Risk Reporting Requirements Technical Review Reports To project and Technical Data Management Process Assessment Results/ Findings To Technical Planning, Risk Management, and Requirements Management Processes Prepare strategy for conducting technical assessments Assess technical work productivity (measure progress against plans) Conduct horizontal and vertical progress technical reviews Assess technical product quality (measure progress against requirements) Capture work pro

## n097 · distractor · test

**Query:** What are key production support criteria ensuring manufacturability and compliance in NASA projects?

- [ ] wrong · n097 · d49a51b8fb2bca02 · *6.2 Technical Team Responsibilities* (p42)
  > Software criteria and products, per NASA-HDBK-2203. 12. *Spectrum (radio frequency)13. High confidence exists that the system requirements will be met in the final production configuration. 1. Adequate resources are in place to support production. 2. The program/project cost and schedule estimates are credible and within program/project constraints. 3. Design-for-manufacturing considerations have been incorporated to ensure ease and efficiency of production and assembly. 4. The product is deemed manufacturable. Evidence is provided that the program/project is compliant with NASA and Implementi

- [ ] wrong · n097 · 98906721297cd62f · *6.2 Technical Team Responsibilities* (p42)
  > Table G-8 – PRR Entrance and Success Criteria Production Readiness Review Entrance Criteria Success Criteria The significant production engineering problems and nonconformances encountered during development are resolved. 1. The design documentation needed to support production is available. 2. The production plans (including but not limited to critical process controls, control limits, and procedures) and preparation to begin fabrication are developed. 3. The production-enabling products are ready. 4. Raw materials are approved and certified. 5. Resources are available, have been allocated, a

- [ ] wrong · n097 · 931ee63fbfc54534 · *Appendices > E. Addressing the Six Life-Cycle Review Criteria* (p447)
  > for projects developing multiple similar flight or ground support systems. To evaluate the degree to which the production plans meet the system’s opera- tional support requirements. Changes in project scope affecting program requirements and constraints have been approved and documented and have been implemented in the design. Acquisitions, partnerships, agreements, and plans are in place to complete the remaining phases. Project design is sufficiently mature to proceed with full-scale production and is consistent with requirements and constraints. Production and remaining life-cycle phases ca

- [ ] wrong · n097 · 31f9b206e55316f1 · *6.2 Technical Team Responsibilities* (p42)
  > Material properties tests are completed along with analyses of loads, stress, fracture control, contamination generation, and other analyses. 13. EEE parts have been selected, and planned testing and delivery will support build schedules. 14. The operational concept has matured, is at a CDR level of detail, and has been considered in test planning. 15. Manufacturability has been adequately included in design. 16. Software components meet the success criteria defined in NASA-HDBK-2203. 17. Human Systems Integration aspects are included in the management and technical planning following guidelin

- [ ] wrong · n097 · e5ea1c774d0125f8 · *6.2 Technical Team Responsibilities* (p42)
  > equipment are available in proper quantities. 9. Production and support staff are qualified. 10. Drawings and/or production models are approved/certified. 11. Production engineering and planning are sufficiently mature for cost-effective 12. NPR 7123.1D -- AppendixG This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7123.1D -- AppendixG Page 89 of 138 consideration assessments. *Updated Human Systems Integration approach. 14. production. Production processes and methods are consistent wit

- [ ] wrong · n097 · b2a4e377dea530b9 · *6.2 Technical Team Responsibilities* (p42)
  > Heritage designs have been suitably assessed for applicability and appropriateness. 16. Manufacturability has been adequately included in design. 17. Software components meet the success criteria defined in NASA-HDBK-2203. 18. Human Systems Integration aspects are included in the management and technical planning following guidelines within NASA/SP-20210010952 and are sufficient to proceed to the next phase 19. Concurrence by the responsible Center spectrum manager that the program/project has provided requisite RF system data. 20. Procurement and supply chain risk management execution is comp

- [ ] wrong · n097 · 5c0899a1b9f4a5cc · *5.0 Product Realization > 5.1 Product Implementation > 5.1.1 Process Description* (p89)
  > technical team should first ensure that the enabling products are ready. This may include ensuring all piece parts are available, drawings are complete and adequate, software design is complete and reviewed, machines to cut the material are available, interface specifications are approved, operators are trained and available, manufacturing and/or coding procedures/ processes are ready, software personnel are trained and available to generate code, test fixtures are devel- oped and ready to hold products while being gener - ated, and software test cases are available and ready to begin model ge

## n045 · paraphrase · test

**Query:** What are some key NASA documents and presentations on cost and risk management in space missions?

- [ ] wrong · n045 · 839626f4cf628be9 · *Appendix T: Systems Engineering in Phase E* (p264)
  > Reserve Guidelines,” by Emmons, D. L., R.E. Bitten, and C.W. Freaner. IEEE Conference Publication pages: 1–16, 2008. Also presented at the NASA Cost Symposium, Denver CO, July 17–19, 2007 NASA Cost Symposium 2014, NASA “Mass Growth Analysis: Spacecraft & Subsystems.” LaRC, August 14th, 2014. Presenter: Vincent Larouche – Tecolote Research, also James K. Johnson, NASA HQ Study Point of Contact Planetary Science Subcommittee, NASA Advisory Council, 23 June, 2008, NASA GSFC. NASA/ Aerospace Corp. presentation; “An Assessment of the Inherent Optimism in Early Conceptual Designs and its Effect on C

- [ ] wrong · n045 · 6dcd17aade52446d · *Preface* (p15)
  > exciting and healthy space program of the future. This handbook provides implementation guidance for NPR 7120.5E, NASA Space Flight Program and Project Management Requirements , which changed and streamlined key procedural requirements across the Agency for space flight program and project management. The goal of the NPR requirements is to ensure programs and projects are developed and successfully executed in the most cost-effective and efficient manner possible. This handbook provides context, rationale, and explanation to facilitate the application of requirements so that they make sense an

- [ ] wrong · n045 · be8d28521365a887 · *Appendix T: Systems Engineering in Phase E* (p264)
  > Benefit-Cost Analysis of Federal Programs” (10/29/1992) Joint (cost and schedule) Confidence Level (JCL). Frequently asked questions (FAQs) can be found at: http://www.nasa.gov/pdf/394931main_JCL_ FAQ_10_12_09.pdf The U. S. Chemical Safety Board (CSB) case study reports on mishaps found at: http://www.csb.gov/ Section 6.3 Interface Management NPR 7120.5, NASA Space Flight Program and Project Management Requirements Section 6.4 Technical Risk Management NPR 8000.4, Agency Risk Management Procedural Requirements NASA/SP-2010-576, NASA Risk-Informed Decision Making Handbook References Cited NASA/

- [ ] wrong · n045 · 67992636f3e8ea60 · *Appendix T: Systems Engineering in Phase E* (p264)
  > NASA Financial Management Requirements (FMR) Volume 4 Special Publications NASA/SP-2010-576 NASA Risk-Informed Decision Making Handbook NASA/SP-2012-599, NASA’s Earned Value Management (EVM) Implementation Handbook NASA/SP-2010-3403, NASA Schedule Management Handbook NASA/SP-2010-3404, NASA Work Breakdown Structure Handbook NASA/SP-2010-3406, Integrated Baseline Review (IBR) Handbook NA SA /SP-2010 -3 407, Human Integration Design Handbook (HIDH) NASA/SP-2011-3421, Probabilistic Risk Assessment Procedures Guide for NASA Managers and Practitioners NASA/SP-2011-3422, NASA Risk Management Handboo

- [ ] wrong · n045 · e3d00c7e9567cb42 · *6.2 Technical Team Responsibilities* (p42)
  > NPR 8705.2, Human-Rating Requirements for Space Systems. NPR 8820.2, Facility Project Requirements (FPR). NASA/SP-2010-3404, Work Breakdown Structure (WBS) Handbook. NASA/SP-2010-576, NASA Risk-Informed Decision Making Handbook. NASA/SP-2014-3705, NASA Spaceflight Program & Project Management Handbook. NASA/SP-2011-3422, NASA Risk Management Handbook. NASA/SP-20210010952, NASA Human Systems Integration (HSI) Handbook. NASA/SP-2016-6105, NASA Systems Engineering Handbook. NASA/SP-2016-6105-SUPPL, Expanded Guidance for NASA Systems Engineering. NASA-STD-3001, NASA Space Flight Human System Stand

- [ ] wrong · n045 · c17377ec69d7f554 · *6.2 Technical Team Responsibilities* (p42)
  > ISO/IEEE 15288 Systems and Software Engineering - System Life-Cycle Processes ISO/IEEE 16085 Systems and Software Engineering - Risk Management ISO/IEEE 29148 Systems and Software Engineering - Requirements Engineering MIL-STD-31000 Department of Defense Standard Practice Technical Data Packages NASA/SP-2010-576 NASA Risk-Informed Decision Making Handbook NASA/SP-2011-3422 NASA Risk Management Handbook NASA/SP-2016-6105 NASA Systems Engineering Handbook NASA/SP-20210010952 NASA Human Systems Integration (HSI) Handbook NASA-HDBK-2203 NASA Software Engineering Handbook NASA-HDBK-7009 NASA Handbo

- [ ] wrong · n045 · 7df3727ee59267f8 · *1.5 Formats for Non-Control Plan I-Table Products* (p133)
  > nn. NASA-STD-8709.22, Safety and Mission Assurance Acronyms, Abbreviations, and Definitions. oo. NASA-STD-8719.14, Process for Limiting Orbital Debris. pp. NASA-STD-8719.24, NASA Expendable Launch Vehicle Payload Safety Requirements. qq. NASA-STD-8729.1, NASA Reliability and Maintainability (R&M) Standard for Spaceflight and Support Systems. rr. NASA-STD-8739.8, Software Assurance and Software Safety Standard. ss. NASA/SP-2016-6105 Rev 2, NASA Systems Engineering Handbook. https://ntrs.nasa.gov/api/citations/20170001761/downloads/20170001761.pdf tt. NASA/SP-2011-3422, NASA Risk Management Hand

- [ ] wrong · n045 · c8badb3ef2c21a17 · *Appendix T: Systems Engineering in Phase E* (p264)
  > NPR 7120.11, NASA Health and Medical Technical Authority (HMTA) Implementation NPR 7123.1, Systems Engineering Processes and Requirements NPR 7150.2, NASA Software Engineering Requirements NPR 8000.4, Risk Management Procedural Requirements NPI 8020.7, NASA Policy on Planetary Protection Requirements for Human Extraterrestrial Missions NPR 8020.12, Planetary Protection Provisions for Robotic Extraterrestrial Missions APR 8070.2, EMI/EMC Class D Design and Environmental Test Requirements. NASA Ames Research Center (ARC) NPR 8580.1, Implementing the National Environmental Policy Act and Executiv

## n022 · exact_id · test

**Query:** ETA-approved Configuration Management process

- [ ] wrong · n022 · f1db4fc2e341113c · *3.2 Common Technical Processes Requirements* (p24)
  > 3.2.15.1 Program/Project Managers shall identify and implement an ETA-approved Configuration Management process to include activities, requirements, guidelines, and documentation, as tailored and customized for configuration management [SE-20]. 3.2.15.2 The Configuration Management process for end products, enabling products, and other work products placed under configuration control is used to: a. Identify the items to be placed under configuration control. b. Identify the configuration of the configuration item at various points in time. c. Systematically control changes to the configuration

- [ ] wrong · n022 · 15f1b502495dc710 · *6.2 Technical Team Responsibilities* (p42)
  > are captured and reported to program/project management who will be developing the overall risk posture. SE-20 3.2.15.1 Program/Project Managers shall identify and implement an ETA-approved Configuration Management process to include activities, requirements, guidelines, and This requirement ensures that the program/project and the ETA identifies how they will perform configuration management of the end products, enabling NPR 7123.1D -- AppendixH This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. C

## n101 · distractor · test

**Query:** How does the Project Plan relate to the Formulation Agreement in project execution?

- [ ] wrong · n101 · aeeb1df6ce8ec665 · *10.0 LIFE-CYCLE REVIEWS* (p94)
  > may use the preliminary Project or Single-Project Program Plan to describe and control the project's or single-project program's execution as long as the Project or Single-Project Program Plan does not conflict with the Formulation Agreement. F.2 Formulation Agreement Title Page Figure F-1 Formulation Agreement Title Page F.3 Formulation Agreement Template [Project or Single-Project Program Name] Formulation Agreement [short title or acronym]

- [ ] wrong · n101 · 7e07c06cc529e20a · *4 Project Life Cycle, Oversight, and Activities by Phase > 4.3 Project Formulation > 4.3.4 Project Phase A, Concept and Technology Development Activities* (p171)
  > Table I-5, and Table 4-7 at the end of this chapter, show which of the control plans are required during this phase and also describes when the control plans are required to be developed. Each of these control plans is described in this chapter, and some of them are required to be baselined before the Project Plan is fully finished and baselined at PDR. These early control plans help the project team manage its early work and become part of the prelimi - nary Project Plan. During Phase B, there is an overlap between the Formula - tion Agreement and the preliminary Project Plan. The Formulation

- [ ] wrong · n101 · 98b4f68efa464754 · *4 Project Life Cycle, Oversight, and Activities by Phase > 4.3 Project Formulation > 4.3.6 Project Phase B, Preliminary Design and Technology Completion Activities* (p196)
  > prescribed requirements with waivers or deviations that are updated and reflected in modifications to the Formulation Agreement. Approved waivers and deviations that apply to project activities during Implementation are documented in the Project Plan. In coordination with the program manager, the MDAA, and the NASA Headquarters Office of International and Interagency Relations (OIIR), the project manager supports the finalization and baselining of external agree - ments, such as interagency and international agreements (including the planning and negotiation of agreements and recommendations o

## n048 · paraphrase · test

**Query:** How does software engineering ensure a product meets user needs and requirements?

- [ ] wrong · n048 · b3eb4a548020a076 · *6.2 Software Engineering Product Content* (p45)
  > software engineering--Life cycle management--Part 1: Guide for life cycle management, 2.61), (2) NPR 7150.2D -- AppendixA This document does not bind the public, except as authorized by law or as incorporated into a contract. This document is uncontrolled when printed. Check NPR 7150.2D -- AppendixA Page 51 of 89 process of providing evidence that the system, software, or hardware and its associated products satisfy requirements allocated to it at the end of each life cycle activity, solve the right problem (e.g., correctly model physical laws, implement business rules, and use the proper syst

- [ ] wrong · n048 · af659ed6ce1d9465 · *5.0 Product Realization > 5.4 Product Validation > 5.4.1 Process Description* (p109)
  > firm that products at each layer of the sys - tem structure meet the capability and other operational expectations of the customer/ user/operator and other interested parties for that product. 5.0 Product Realization • To ensure the human has been properly integrated into the system: » The user interface meets human engineering criteria. » Operators and maintainers have the required skills and abilities. » Instructions are provided and training pro - grams are in place. » The working environment supports crew health and safety. • To ensure that any problems discovered are appropriately resolve

- [ ] wrong · n048 · 9566d47feeae4861 · *4.1 Software Requirements* (p32)
  > 4.1.1 The requirements phase is one of the most critical phases of software engineering. Studies show that the top problems in the software industry are due to poor requirements elicitation, inadequate requirements specification, and inadequate management of changes to requirements. Requirements provide the foundation for the entire life cycle, as well as for the software product. Requirements also provide a basis for planning, estimating, and monitoring. Requirements are based on customer, user, and other stakeholder needs and design and development constraints. The development of requirement

- [ ] wrong · n048 · deb4011d1b4f0594 · *4.0 System Design Processes > 4.2 Technical Requirements Definition > 4.2.1 Process Description* (p64)
  > the requirements will assist the potential users in determining if the product specified meets their needs or how the product should be modified to meet their needs. During system design, requirements are allocated to subsystems (e.g., hardware, software, and other major components of the system), people, or processes. Reduce the development effort because less rework is required to address poorly written, missing, and misunderstood requirements The Technical Requirements Definition Process activities force the relevant stakeholders to rigorously consider all of the requirements before design 

- [ ] wrong · n048 · 107ef809a617d576 · *6.1 Software Engineering Products* (p44)
  > It is possible to prepare a plan, associated procedures, and reports, as well as numerous records, requests, descriptions, and specifications for each software development life cycle process. When deciding how to prepare any of these items, consider the users of the information first. Reviewing and understanding the requirements, needs, and background of users and stakeholders are essential to applying the recommendations for the content of software records defined in NASA-HDBK-2203. Specific content within these records may not apply to every project. Use of NASA Center and contractor formats

- [ ] wrong · n048 · 613b077d30a17929 · *4.1 Software Requirements* (p32)
  > 4.1.3 The project manager shall perform software requirements analysis based on flowed-down and derived requirements from the top-level systems engineering requirements, safety and reliability analyses, and the hardware specifications and design. [SWE-051] 4.1.4 The project manager shall include software related safety constraints, controls, mitigations, and assumptions between the hardware, operator, and software in the software requirements documentation. [SWE-184] 4.1.5 The project manager shall track and manage changes to the software requirements. [SWE-053] 4.1.6 The project manager shall

- [ ] wrong · n048 · 0b32c7daec81f37b · *6.2 Software Engineering Product Content* (p45)
  > Procedural Requirements). Unit Test. (1) Testing of individual routines and modules by the developer or an independent tester (ISO/IEC/IEEE 24765). (2) A test of individual programs or modules in order to ensure that there are no analysis or programming errors (ISO/IEC 2382-20). (3) Test of individual hardware or software units or groups of related units. (ISO/IEC/IEEE 24765) Validation. (1) Confirmation, through the provision of objective evidence, that the requirements for a specific intended use or application have been fulfilled (ISO/IEC 25000:2014 Systems and software Engineering--Systems

- [ ] wrong · n048 · 061bc6356c149bf6 · *4.0 System Design Processes > 4.2 Technical Requirements Definition > 4.2.1 Process Description* (p64)
  > assumptions; and (c) are essential to and consis - tent with designing and realizing the appropriate product solution form that will satisfy the appli - cable product life cycle phase success criteria. 3. Do the Requirements Satisfy Stakeholders? All relevant stakeholder groups identify and remove defects. 4. Are the Requirements Feasible? All require - ments should make technical sense and be possi- ble to achieve. 5. Are the Requirements Verifiable? All require - ments should be stated in a fashion and with enough information that it will be possible to verify the requirement after the end p

- [ ] wrong · n048 · e287221f2e43013d · *6.2 Software Engineering Product Content* (p45)
  > customers. (A Guide to the Project Management Body of Knowledge (PMBOK(R) Guide) -- Fifth Edition), and (4) process of evaluating a system or component during or at the end of the development process to determine whether it satisfies specified requirements (IEEE 1012-2016, IEEE Standard for Software Verification and Validation, 3.1) Note: Validation in a system life cycle context is the set of activities ensuring and gaining confidence that a system is able to accomplish its intended use, goals, and objectives. The right system has been built. Validation demonstrates that the system can be use

- [ ] wrong · n048 · 569d54bf004baffc · *6.2 Software Engineering Product Content* (p45)
  > under the terms of the contract or an organization or part of an organization or individual that enters into an agreement with the application management organization for the supply of a software product or software service. Software Suppliers includes NASA in-house software development. Software Validation. Confirmation that the product, as provided (or as it will be provided), fulfills its intended use. In other words, validation ensures that “you built the right thing.” (Source: IEEE 1012, IEEE Standard for Software Verification and Validation) Software Verification. Confirmation that produ

- [ ] wrong · n048 · d8cce0240a0edcb2 · *4.1 Software Requirements* (p32)
  > 4.1.2 The project manager shall establish, capture, record, approve, and maintain software requirements, including requirements for COTS, GOTS, MOTS, OSS, or reused software components, as part of the technical specification. [SWE-050] Note: The software technical requirements definition process is used to transform the baselined stakeholder expectations into unique, quantitative, and measurable technical software requirements that can be used for defining a design solution for the software end products and related enabling products. This process also includes validation of the requirements to

