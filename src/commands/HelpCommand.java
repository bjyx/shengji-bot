package commands;

import java.util.*;

import net.dv8tion.jda.core.MessageBuilder;
import net.dv8tion.jda.core.entities.*;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;

public class HelpCommand extends Command {
	private TreeMap<String, Command> commands;
	
	public HelpCommand() {
		commands = new TreeMap<>();
	}
	
	public Command registerCommand(Command command) {
		commands.put(command.getAliases().get(0), command);
		return command;
	}
	
	@Override
	public void onCommand(MessageReceivedEvent e, String[] args) {
		MessageChannel channel = e.getTextChannel();
		if (args.length < 2)
        {
            StringBuilder s = new StringBuilder();
            for (Command c : commands.values())
            {
                String description = c.getDescription();
                description = (description == null || description.isEmpty()) ? "`404 NOT FOUND`" : description;

                s.append("**").append(c.getAliases().get(0)).append("** - ");
                s.append(description).append("\n");
            }

            channel.sendMessage(new MessageBuilder()
                    .append("The following commands are supported by the bot\n")
                    .append(s.toString())
                    .build()).queue();
        }
        else
        {
            String command = args[1].charAt(0) == '.' ? args[1] : "." + args[1];    //If there is not a preceding . attached to the command we are search, then prepend one.
            for (Command c : commands.values())
            {
                if (c.getAliases().contains(command))
                {
                    String name = c.getName();
                    String description = c.getDescription();
                    List<String> usageInstructions = c.getUsageInstructions();
                    name = (name == null || name.isEmpty()) ? "`null`" : name;
                    description = (description == null || description.isEmpty()) ? "`404 NOT FOUND`" : description;
                    usageInstructions = (usageInstructions == null || usageInstructions.isEmpty()) ? Collections.singletonList("404 NOT FOUND") : usageInstructions;
                    channel.sendMessage(new MessageBuilder()
                            .append("**Name:** " + name + "\n")
                            .append("**Description:** " + description + "\n")
                            .append("**Usage:** ")
                            .append(usageInstructions.get(0))
                            .build()).queue();
                    for (int i = 1; i < usageInstructions.size(); i++)
                    {
                        channel.sendMessage(new MessageBuilder()
                            .append("__" + name + " Usage Cont. (" + (i + 1) + ")__\n")
                            .append(usageInstructions.get(i))
                            .build()).queue();
                    }
                    return;
                }
            }
            channel.sendMessage(new MessageBuilder()
                    .append("The provided command '**" + args[1] + "**' does not exist. Use .help to list all commands.")
                    .build()).queue();
        }

	}

	@Override 
    public List<String> getAliases()
    {
        return Arrays.asList("TS.help", "TS.commands");
    }
	
	@Override
	public String getName() {
		return "HelpHelp (help, commands)";
	}
	
	@Override
	public String getDescription() {
		return "Get some help with commands.";
	}

	@Override
	public List<String> getUsageInstructions() {
        return Collections.singletonList(
                "TS.help   **OR**  TS.help *<command>*\n"
                + "TS.help - returns the list of commands along with a simple description of each.\n"
                + "TS.help <command> - returns the name, description, aliases and usage information of a command.\n"
                + "   - This can use the aliases of a command as input as well.\n"
                + "__Example:__ TS.help help");
	}
}
