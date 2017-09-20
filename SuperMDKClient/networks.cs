using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;
using System.Net;

namespace networks
{
    public class udpclient
    {
        UdpClient udp;
        public string recvstr = "";
        private int port;
        public void udpinit(int port)
        {
            this.port = port;
            udp = new UdpClient(port);
        }
        public string ReceiveData()
        {

            try
            {
                IPEndPoint anyip = new IPEndPoint(IPAddress.Any, 0);
                byte[] buffer = udp.Receive(ref anyip);
                recvstr = Encoding.UTF8.GetString(buffer);

            }
            catch (Exception ex)
            {

            }
            return recvstr;


        }
        public void socketClose()
        {
            if (udp != null)
            {
                udp.Close();
            }
        }
    }

    public class DataClass
    {

        private float[] rotations = new float[30];
        /*
         * 0-2 left arm1 node rotation x,y,z
         * 3-5 left arm2 node rotation x,y,z
         * 6-8 right arm1 node rotation x,y,z
         * 9-11 right arm2 node rotation x,y,z
         * 12-14 left leg node rotation x,y,z
         * 15-17 right leg node rotation x,y,z
         * 18-20 head node rotation x,y,z
         * 
         */
        public bool ischange = false;
        private string Com;
        public int Error_num = 0;
        public DataClass(string coms)
        {
            this.Com = coms;
        }
        public bool GetComChange(string Com)
        {

            this.Com = Com;
            Error_num = -1;
            if (Com[0] != '<' || Com[Com.Length - 1] != '>')
            {
                return false;
            }
            Com = Com.Substring(1, 167);
            string[] ComChange = Com.Split('!');
            for (int i = 0; i < 7; i++)
            {
                if (ComChange[i].Contains("Error"))
                {

                    Error_num = i;
                    return false;
                }
            }
            for (int i = 0; i < 7; i++)
            {
                string[] strRotation = ComChange[i].Split('|');
                float[] fRotation = new float[3];
                for (int j = 0; j <= 2; j++)
                {
                    if (strRotation[j][0] == '+')
                    {
                        fRotation[j] = float.Parse(strRotation[j].Substring(1, 6));
                    }
                    else
                    {
                        fRotation[j] = float.Parse(strRotation[j].Substring(1, 6));
                        fRotation[j] = -fRotation[j];
                    }
                }
                switch (i)
                {
                    case 0:
                        this.rotations[0] = fRotation[0];
                        this.rotations[2] = fRotation[1];
                        this.rotations[1] = fRotation[2];
                        break;
                    case 1:
                        this.rotations[3] = fRotation[0];
                        this.rotations[5] = fRotation[1];
                        this.rotations[4] = 180 + fRotation[2];
                        break;
                    case 2:
                        this.rotations[9] = fRotation[0];
                        this.rotations[11] = fRotation[1];
                        this.rotations[10] = 180 + fRotation[2];
                        break;
                    case 3:
                        this.rotations[6] = fRotation[0];
                        this.rotations[8] = fRotation[1];
                        this.rotations[7] = fRotation[2];
                        break;
                    case 4:
                        this.rotations[12] = fRotation[0];
                        this.rotations[14] = fRotation[1];
                        this.rotations[13] = fRotation[2];
                        break;
                    case 5:
                        this.rotations[15] = fRotation[0];
                        this.rotations[17] = fRotation[1];
                        this.rotations[16] = fRotation[2];
                        break;
                    case 6:
                        this.rotations[18] = fRotation[0];
                        this.rotations[20] = 0f;
                        this.rotations[19] = fRotation[2];
                        break;
                }
            }
            return true;
        }

        public float[] getLeftArm()
        {
            float[] leftArm = new float[6];
            for (int i = 0; i <= 5; i++)
            {
                leftArm[i] = this.rotations[i];
            }
            return leftArm;

        }
        public float[] getLeftlegRotation()
        {
            float[] leftLeg = new float[3];
            for (int i = 12; i <= 14; i++)
            {
                leftLeg[i - 12] = rotations[i];
            }
            return leftLeg;
        }
        public float[] getRightLegRotation()
        {
            float[] rightLeg = new float[3];
            for (int i = 15; i <= 17; i++)
            {
                rightLeg[i - 15] = this.rotations[i];
            }
            return rightLeg;
        }
    }
}