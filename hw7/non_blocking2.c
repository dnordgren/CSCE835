#include "mpi.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char** argv)
{
	int rank, size;
	MPI_Request *requestList,requestNull;
	MPI_Status  status;
	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &size);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	if( rank == 0 )
	{
		int dataOut=13, dataIn, pr;
		requestList =(MPI_Request*)malloc((size-1)*sizeof(MPI_Request));
		for(pr=1;pr<size;pr++)
		{
			MPI_Isend(&dataOut,1,MPI_INT,pr,0,MPI_COMM_WORLD, &requestNull);
		}
		for(pr=1;pr<size;pr++)
		{
			MPI_Irecv(&dataIn,1,MPI_INT,pr,1,MPI_COMM_WORLD,&(requestList[pr-1]));
		}
		int prW;
		for(prW=1;prW<size;prW++)
		{
			int index;
			MPI_Waitany(size-1, requestList, &index, &status);
			printf("From the process%d: %d\n", index+1, dataIn);
		}
	}
	else
	{
		int message;
		MPI_Status  status;
		MPI_Recv(&message,1,MPI_INT,0,0,MPI_COMM_WORLD,&status);
		message =message*rank;
		MPI_Send(&message,1,MPI_INT,0,1,MPI_COMM_WORLD);
	}
	MPI_Finalize();
	return 0;
}
