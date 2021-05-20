## PLAN

May 24 -May 30:	
[ ]Evaluate the version changes, 
[ ]Evaluate the OpenNMT commandlines	
[ ]Compare the 2 OpenNMT versions and list all changes 
    a.	Translator model changes 
    b.	Preprocess model changes to build vocabulary
    c.	Parameter changes
    d.	Lib dependency changes
    e.	Any new features which may be relevant to our system
 [ ]3 system commands being used currently from OpenNMT-py. Need to understand all the parameters being passed to them and their use/relevance to our translation
----
May 31- June 6 : Lib dependency updates, 
[ ]Onmt Logger updates	
[ ]Other libraries like torch , etc and their versions being used in the system need to be updated to be compatible with the requirements of OpenNMT 2.0
----
June 7-  June 13 : Query Generator updates	
[ ]Query Generator utilizes the ONMT preprocess command
[ ]Evaluate the changes made to it in the new version as well as check build vocab utility here. 
[ ]Update the system to make it latest system compatible
----
June 14 - June 20 : Review Week	
[ ]Review on the progress so far
[ ]Feedback from Adrian
[ ]Implement feedback
[ ]Complete anything pending so far
----
June 21 - June 27 :
[ ]Train Models update	
[ ]Update the training module where onmt train is being called.
----
June 28 - July 4 :	Translation Script update	
[ ]Update the onmt translate commandlines
----
July 5 - July 11 :	Validation Week 	
[ ]Unit Testing for every module updated so far 
[ ]entire system model run for continuous Integration and Regression.
----
July 12 - July 18 : Review Week 	
[ ]Review on the progress so far
[ ]Feedback from Adrian
[ ]Complete anything pending so far
----
July 19 - July 25 : Feedback implementation
[ ]Self Re-review	
[ ]Feedback implementation
[ ]Re-validations of the system
----
July 26 - Aug 1 : Final Review	
[ ]Final Review with Adrian on the latest system post migration and validation
----
Aug 2 - Aug 8 :	Documentation
[ ]Documentation of the entire system and our efforts during this project. 
Note : This is an ongoing process
----
Aug 9 - Aug 15 : Discussion on potential new features	
[ ]Talk with mentors and interested people in the community about potential improvements in the software. 
Note: This will happen if rest of tasks finish according to plan. This is an extension.
----
Aug 16 - Aug 22 : Development of new feature
[ ]Decide on one feature with my mentor and work on the design + development of the same
----
Aug 23 - Aug 24	: Validation and documentation of the new feature
[ ]Validation of the new feature as well as continuous documentation of all our efforts + progress on the feature. Also the pending tasks. 
----