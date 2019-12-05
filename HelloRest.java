package com.tt;

import java.util.ArrayList;
import java.util.List;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;



@Path("/Hello")
public class HelloRest {
	
/*
     @GET  
	  @Path("/str")
	  @Produces(MediaType.TEXT_PLAIN)  
	    public String getIt() {
	        return "Got it!";
	    }*/
	
	@GET
	@Path("{name}/{country}")	
	public Response getUserById( @PathParam("name") String name, @PathParam("country") String country) {

		 String op= name+"-->"+country;
		return Response.status(200).entity(op).build();
	}
}
