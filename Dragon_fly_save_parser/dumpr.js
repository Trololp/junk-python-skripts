var hexString;

decimalToHexString = function(number, N)
{
  if (number < 0)
  {
	  if(N == 8)
	  {
		number = 0xFFFFFFFF + number + 1;  
	  }
	if(N == 4)
	{
		number = 0xFFFF + number + 1;
	}
  }

  var num_str = number.toString(16).toUpperCase();
  var num_len = num_str.length;
  if (num_len <= N-1)
  {
	  for(let i = num_len; i <= N-1; i++)
	  {num_str = '0'+num_str;}
	  
  }
  num_str = num_str + ' ';
  
  return num_str;
  
}

heap32_to_hex = function(start_index, size)
{
	var hexString = '';
	i = start_index;
	for(; i < start_index + size; i++)
	{
		var hexString = hexString + decimalToHexString(HEAP32[i], 8);
		if ((i - start_index) % 4 == 0)
		{
			hexString = hexString + '\n';
		}
	}
	
	return hexString;
};

heap16_to_hex = function(start_index, size)
{
	var hexString = '';
	i = start_index;
	for(; i < start_index + size; i++)
	{
		var hexString = hexString + decimalToHexString(HEAP16[i], 4);
		if ((i - start_index) % 8 == 0)
		{
			hexString = hexString + '\n';
		}
	}
	
	return hexString;
};